import json
import os
from pathlib import Path
import random
import shutil

plu_mapping = {
    '4011': 'Bananer Bama',
    '4015': 'Epler Røde',
    '4088': 'Paprika Rød',
    '4196': 'Appelsin',
    '94011': 'Bananer Økologisk',
    '90433917': 'Red Bull Regular 250ml boks',
    '90433924': 'Red Bull Sukkerfri 250ml boks',
    '7020097009819': 'Karbonadedeig 5% u/Salt og Vann 400g Meny',
    '7020097026113': 'Kjøttdeig Angus 14% 400g Meny',
    '7023026089401': 'Ruccula 65g Grønn&Frisk',
    '7035620058776': 'Rundstykker Grove Fullkorn m/Frø Rustikk 6stk 420g',
    '7037203626563': 'Leverpostei Ovnsbakt Orginal 190g Gilde',
    '7037206100022': 'Kokt Skinke Ekte 110g Gilde',
    '7038010009457': 'Yoghurt Skogsbær 4x150g Tine',
    '7038010013966': 'Norvegia 26% skivet 150g Tine',
    '7038010021145': 'Jarlsberg 27% skivet 120g Tine',
    '7038010054488': 'Cottage Cheese Mager 2% 400g Tine',
    '7038010068980': 'Yt Protein Yoghurt Vanilje 430g Tine',
    '7039610000318': 'Frokostegg Frittgående L 12stk Prior',
    '7040513000022': 'Gulrot 750g Beger',
    '7040513001753': 'Gulrot 1kg pose First Price',
    '7040913336684': 'Evergood Classic Filtermalt 250g',
    '7044610874661': 'Pepsi Max 0,5l flaske',
    '7048840205868': 'Frokostyoghurt Skogsbær 125g pose Q',
    '7071688004713': 'Original Havsalt 190g Sørlandschips',
    '7622210410337': 'Kvikk Lunsj 3x47g Freia'
}
# Define your original data path and new (global) data path
data_path = Path("../../../data/images/NGD_HACK")
new_data_path = Path("../../../new_data/YOLO_format")

# Create the global directories:
global_img_train_dir = new_data_path / "images" / "train"
global_img_val_dir   = new_data_path / "images" / "val"
global_labels_train_dir = new_data_path / "labels" / "train"
global_labels_val_dir   = new_data_path / "labels" / "val"

for d in [global_img_train_dir, global_img_val_dir, global_labels_train_dir, global_labels_val_dir]:
    d.mkdir(parents=True, exist_ok=True)

def copy_files_global(files, img_dest, label_dest, orig_prod_dir, product_code):
    for filename in files:
        # Optionally, prefix the filename with the product code if not already included.
        new_filename = f"{product_code}_{filename}" if not filename.startswith(product_code) else filename

        src_image = orig_prod_dir / filename
        dest_image = img_dest / new_filename
        shutil.copy(src_image, dest_image)

        base_name = filename.rsplit(".", 1)[0]
        new_base_name = f"{product_code}_{base_name}" if not base_name.startswith(product_code) else base_name
        annot_file = base_name + ".txt"
        new_annot_file = new_base_name + ".txt"
        src_label = orig_prod_dir / annot_file
        if src_label.exists():
            dest_label = label_dest / new_annot_file
            shutil.copy(src_label, dest_label)
        else:
            print(f"Annotation file not found for {filename}")

def process_folder_global(mapping):
    for product_code, product_name in mapping.items():
        print("Processing product:", product_code, product_name)
        orig_prod_dir = data_path / product_code
        print("Looking for original directory:", orig_prod_dir.resolve())

        if not orig_prod_dir.exists():
            print("Original path does not exist:", orig_prod_dir)
            continue

        # Get all image files (ignoring visualization files ending with "_bb.png")
        image_files = [f for f in os.listdir(orig_prod_dir)
                       if f.endswith(".png") and not f.endswith("bb.png")]
        random.shuffle(image_files)

        # 60% training, 40% validation split
        split_idx = int(0.6 * len(image_files))
        train_files = image_files[:split_idx]
        val_files = image_files[split_idx:]

        copy_files_global(train_files, global_img_train_dir, global_labels_train_dir, orig_prod_dir, product_code)
        copy_files_global(val_files, global_img_val_dir, global_labels_val_dir, orig_prod_dir, product_code)

#process_folder_global(plu_mapping)
print("Dataset reconstruction complete")

def convert_json_annotation(json_file: Path)-> list:
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    img_details = data["image_details"][0]

    img_width = int(img_details["width"].replace("px", ""))
    img_height = int(img_details["height"].replace("px", ""))

    print(f"Image width: {img_width}")
    print(f"Image height: {img_height}")


    yolo_lines=[]
    for obj in data["label"]:
        product_code = obj["label"]

        topX = obj["topX"]
        topY = obj["topY"]
        bottomX = obj["bottomX"]
        bottomY = obj["bottomY"]
        x_center = (topX + bottomX) / 2.0
        y_center = (topY + bottomY) / 2.0
        bbox_width = bottomX - topX
        bbox_height = bottomY - topY

        line = f"{product_code} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"
        yolo_lines.append(line)
    return yolo_lines



    # Example usage:
    # Assuming you have an annotation file "4011-42.txt" in your working directory
annotation_path = Path("../../../new_data/YOLO_format/labels")

def process_label_files(directory: Path):
    for txt_file in directory.glob("*.txt"):
        print("Processing file:", txt_file)
        try:
            yolo_lines = convert_json_annotation(txt_file)
            # Overwrite the file with the new YOLO formatted annotation
            with txt_file.open("w", encoding="utf-8") as f:
                f.write("\n".join(yolo_lines))
            print("File updated:", txt_file)
        except Exception as e:
            print(f"Failed to process {txt_file}: {e}")

# Define your train and validation directories
train_dir = Path("../../../new_data/YOLO_format/labels/train")
val_dir = Path("../../../new_data/YOLO_format/labels/val")

# Process both directories
process_label_files(train_dir)
process_label_files(val_dir)

print("Dataset reconstruction complete")
