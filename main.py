from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
import numpy as np
import os
from matplotlib import font_manager

# === Paramètres ===
text = "Quelqu’un t’aime"
font_name = "Arial"  # Change ici avec le nom exact de ta police ou un chemin absolu vers un .ttf
font_size = 100
text_color = "white"
stroke_color = "black"
stroke_width = 2
duration = 5  # secondes
fps = 30
video_size = (1920, 1080)

# === Chercher le chemin de la police installée ===
font_paths = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
font_path = next((p for p in font_paths if font_name.lower() in os.path.basename(p).lower()), None)

if font_path is None:
    raise ValueError(f"Police '{font_name}' introuvable sur le système. Donne plutôt un chemin vers le .ttf.")

font = ImageFont.truetype(font_path, font_size)

# === Générer les frames ===
total_frames = int(duration * fps)
letters = list(text)
letters_per_frame = len(letters) / total_frames
frames = []

for frame_number in range(total_frames):
    img = Image.new("RGBA", video_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    num_letters = int(letters_per_frame * frame_number)
    current_text = ''.join(letters[:num_letters])

    if current_text:
        text_width, text_height = draw.textsize(current_text, font=font)
        position = ((video_size[0] - text_width) // 2, (video_size[1] - text_height) // 2)
        draw.text(position, current_text, font=font, fill=text_color,
                  stroke_width=stroke_width, stroke_fill=stroke_color)

    frames.append(np.array(img))

# === Créer la vidéo avec alpha ===
clip = ImageSequenceClip(frames, fps=fps)
clip.write_videofile(
    "typing_text_alpha.mov",
    codec="libx264",
    fps=fps,
    preset="medium",
    audio=False,
    ffmpeg_params=["-pix_fmt", "yuva420p"]  # Alpha support
)
