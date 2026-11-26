
import sys
import torch

from PIL import Image, ImageDraw, ImageFont
from transformers import AutoTokenizer, BertForMaskedLM

MODEL = "bert-base-uncased"
K = 3

FONT = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 28)
GRID_SIZE = 40
PIXELS_PER_WORD = 200


def main():
    text = input("Text: ")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL, local_files_only=True
    )

    inputs = tokenizer(text, return_tensors="pt")

    mask_token_index = get_mask_token_index(
        tokenizer.mask_token_id, inputs
    )

    if mask_token_index is None:
        sys.exit(f"Input must include {tokenizer.mask_token}.")

    model = BertForMaskedLM.from_pretrained(
        MODEL,
        local_files_only=True,
        attn_implementation="eager"
    )

    model.eval()

    with torch.no_grad():
        result = model(**inputs, output_attentions=True)

    mask_logits = result.logits[0, mask_token_index]
    top_tokens = torch.topk(mask_logits, K).indices.tolist()

    print("\nPredictions:")
    for token in top_tokens:
        print(text.replace(
            tokenizer.mask_token,
            tokenizer.decode([token])
        ))

    print("\nGenerating attention diagrams...")

    visualize_attentions(inputs.tokens(), result.attentions)

    print("All attention diagrams generated successfully.")


def get_mask_token_index(mask_token_id, inputs):
    input_ids = inputs["input_ids"][0].tolist()

    try:
        return input_ids.index(mask_token_id)
    except ValueError:
        return None


def get_color_for_attention_score(attention_score):
    score = float(attention_score)
    intensity = max(0, min(255, int(score * 255)))

    return (intensity, intensity, intensity)


def visualize_attentions(tokens, attentions):
    for layer_index, layer in enumerate(attentions, start=1):
        for head_index in range(layer.shape[1]):
            attention_weights = layer[0, head_index]

            generate_diagram(
                layer_index,
                head_index + 1,
                tokens,
                attention_weights
            )


def generate_diagram(layer_number, head_number, tokens, attention_weights):
    image_size = GRID_SIZE * len(tokens) + PIXELS_PER_WORD

    img = Image.new("RGBA", (image_size, image_size), "black")
    draw = ImageDraw.Draw(img)

    for i, token in enumerate(tokens):
        token_image = Image.new(
            "RGBA", (image_size, image_size), (0, 0, 0, 0)
        )
        token_draw = ImageDraw.Draw(token_image)

        token_draw.text(
            (image_size - PIXELS_PER_WORD,
             PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )

        token_image = token_image.rotate(90)
        img.paste(token_image, mask=token_image)

        _, _, width, _ = draw.textbbox(
            (0, 0), token, font=FONT
        )

        draw.text(
            (PIXELS_PER_WORD - width,
             PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )

    for i in range(len(tokens)):
        y = PIXELS_PER_WORD + i * GRID_SIZE

        for j in range(len(tokens)):
            x = PIXELS_PER_WORD + j * GRID_SIZE

            color = get_color_for_attention_score(
                attention_weights[i][j]
            )

            draw.rectangle(
                (x, y, x + GRID_SIZE, y + GRID_SIZE),
                fill=color
            )

    img.save(
        f"Attention_Layer{layer_number}_Head{head_number}.png"
    )


if __name__ == "__main__":
    main()
