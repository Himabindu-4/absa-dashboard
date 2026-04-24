# wordcloud_visualization.py

import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# =========================
# LOAD DATA (YOUR FILES)
# =========================

df1 = pd.read_excel("app/data/Restaurants_Train_v2.xlsx")
df2 = pd.read_excel("app/data/Laptop_Train_v2.xlsx")

df = pd.concat([df1, df2], ignore_index=True)

# =========================
# CLEAN TEXT
# =========================

def clean_text(text):
    text = str(text)
    text = re.sub(r"<.*?>", "", text)        # remove HTML
    text = re.sub(r"http\S+", "", text)      # remove links
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # remove special chars
    text = text.lower()
    return text

df["clean"] = df["Sentence"].apply(clean_text)

# =========================
# GENERATE WORD CLOUD
# =========================

def generate_wordcloud(text, title):
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="black",
        stopwords=STOPWORDS,
        colormap="viridis"
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=16)
    plt.show()


# =========================
# SPLIT BY SENTIMENT
# =========================

positive_text = " ".join(df[df["polarity"] == "positive"]["clean"])
negative_text = " ".join(df[df["polarity"] == "negative"]["clean"])
neutral_text  = " ".join(df[df["polarity"] == "neutral"]["clean"])

# =========================
# CREATE WORD CLOUDS
# =========================

print("Generating word clouds...")

generate_wordcloud(positive_text, "Positive Reviews Word Cloud")
generate_wordcloud(negative_text, "Negative Reviews Word Cloud")
generate_wordcloud(neutral_text, "Neutral Reviews Word Cloud")

print("Done ✅")