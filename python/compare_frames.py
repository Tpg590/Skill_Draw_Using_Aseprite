from PIL import Image

f1 = Image.open("python/refined_f1.png")
f2 = Image.open("python/refined_f2.png")
f3 = Image.open("python/refined_f3.png")
f4 = Image.open("python/refined_f4.png")

w, h = f1.size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
sheet.paste(f1, (0, 0))
sheet.paste(f2, (w, 0))
sheet.paste(f3, (w * 2, 0))
sheet.paste(f4, (w * 3, 0))

sheet.save("python/compare_sheet.png")
print("Saved compare_sheet.png")
