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

# Define your paths as pathlib.Path objects
data_path = Path("../../../data/images/NGD_HACK")
new_data_path = Path("../../../new_data/YOLO_format")
new_data_path.mkdir(parents=True, exist_ok=True)

def copy_files(files, img_dest, label_dest, orig_prod_dir):
    for filename in files:
        src_image = orig_prod_dir / filename
        dest_image = img_dest / filename
        shutil.copy(src_image, dest_image)

        base_name = filename.rsplit(".", 1)[0]
        annot_file = base_name + ".txt"
        src_label = orig_prod_dir / annot_file
        if src_label.exists():
            dest_label = label_dest / annot_file
            shutil.copy(src_label, dest_label)
        else:
            print(f"Annotation file not found for {filename}")

def process_folder(mapping):
    for product_code, product_name in mapping.items():
        folder_name = product_name.lower().replace(" ", "-")
        new_product_dir = new_data_path / folder_name
        img_train_dir = new_product_dir / "images" / "train"
        img_val_dir = new_product_dir / "images" / "val"
        labels_train_dir = new_product_dir / "labels" / "train"
        labels_val_dir = new_product_dir / "labels" / "val"

        # Create directories for train and validation splits
        img_train_dir.mkdir(parents=True, exist_ok=True)
        img_val_dir.mkdir(parents=True, exist_ok=True)
        labels_train_dir.mkdir(parents=True, exist_ok=True)
        labels_val_dir.mkdir(parents=True, exist_ok=True)

        print("Processing product:", product_code, product_name)
        # Print absolute path of the original directory for debugging
        orig_prod_dir = data_path / product_code
        print("Looking for original directory:", orig_prod_dir.resolve())

        if not orig_prod_dir.exists():
            print("Original path does not exist:", orig_prod_dir)
            continue

        # Get all image files (ignore visualization files ending with "_bb.png")
        image_files = [f for f in os.listdir(orig_prod_dir)
                       if f.endswith(".png") and not f.endswith("bb.png")]
        random.shuffle(image_files)

        # 60% training, 40% validation split
        split_idx = int(0.6 * len(image_files))
        train_files = image_files[:split_idx]
        val_files = image_files[split_idx:]

        copy_files(train_files, img_train_dir, labels_train_dir, orig_prod_dir)
        copy_files(val_files, img_val_dir, labels_val_dir, orig_prod_dir)

process_folder(plu_mapping)


def convert_json_annotation(path):



print("Dataset reconstruction complete")
