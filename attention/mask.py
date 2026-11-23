
import sys
import tensorflow as tf

from PIL import Image, ImageDraw, ImageFont
from transformers import AutoTokenizer, TFBertForMaskedLM

# Pre-trained masked language model
MODEL = "bert-base-uncased"

# Number of predictions to generate
K = 3

# Constants for generating attention diagrams
FONT = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 28)
GRID_SIZE = 40
PIXELS_PER_WORD = 200


def main():
    text = input("Text: ")

    # Tokenize input
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    inputs = tokenizer(text, return_tensors="tf")

    mask_token_index = get_mask_token_index(
        tokenizer.mask_token_id, inputs
    )

    if mask_token_index is None:
        sys.exit(f"Input must include mask token {tokenizer.mask_token}.")

    # Use model to process input
    model = TFBertForMaskedLM.from_pretrained(MODEL)
    result = model(**inputs, output_attentions=True)

    # Generate predictions
    mask_token_logits = result.logits[0, mask_token_index]
    top_tokens = tf.math.top_k(mask_token_logits, K).indices.numpy()

    for token in top_tokens:
        print(text.replace(tokenizer.mask_token, tokenizer.decode([token])))

    # Visualize attentions
    visualize_attentions(inputs.tokens(), result.attentions)


def get_mask_token_index(mask_token_id, inputs):
    """
    Return the index of the token with the specified `mask_token_id`, or
    None if not present in the inputs.
    """
    input_ids = inputs["input_ids"][0].numpy().tolist()

    try:
        return input_ids.index(mask_token_id)
    except ValueError:
        return None


def get_color_for_attention_score(attention_score):
    """
    Return a tuple of three integers representing a shade of gray for the
    given attention_score.
    """
    score = float(attention_score)

    intensity = int(score * 255)

    return (intensity, intensity, intensity)


def visualize_attentions(tokens, attentions):
    """
    Produce a graphical representation of self-attention scores.

    Generate one diagram for every attention head in every layer.
    """
    for layer_number, layer in enumerate(attentions, start=1):

        for head_number in range(layer.shape[1]):

            attention_weights = layer[0][head_number]

            generate_diagram(
                layer_number,
                head_number + 1,
                tokens,
                attention_weights
            )


def generate_diagram(layer_number, head_number, tokens, attention_weights):
    """
    Generate a diagram representing the self-attention scores for a single
    attention head.
    """

    # Create new image
    image_size = GRID_SIZE * len(tokens) + PIXELS_PER_WORD
    img = Image.new("RGBA", (image_size, image_size), "black")
    draw = ImageDraw.Draw(img)

    # Draw each token onto the image
    for i, token in enumerate(tokens):

        # Draw token columns
        token_image = Image.new(
            "RGBA", (image_size, image_size), (0, 0, 0, 0)
        )

        token_draw = ImageDraw.Draw(token_image)

        token_draw.text(
            (
                image_size - PIXELS_PER_WORD,
                PIXELS_PER_WORD + i * GRID_SIZE
            ),
            token,
            fill="white",
            font=FONT
        )

        token_image = token_image.rotate(90)
        img.paste(token_image, mask=token_image)

        # Draw token rows
        _, _, width, _ = draw.textbbox((0, 0), token, font=FONT)

        draw.text(
            (
                PIXELS_PER_WORD - width,
                PIXELS_PER_WORD + i * GRID_SIZE
            ),
            token,
            fill="white",
            font=FONT
        )

    # Draw each word
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

    # Save image
    img.save(f"Attention_Layer{layer_number}_Head{head_number}.png")


if __name__ == "__main__":
    main()

