"""Create a bag of 5-letter words used by Wordle game."""
import pandas as pd


def save_words_with_likelihood(df, destination):
    df["likelihood"] = df["count"].div(df["count"].sum())
    df[["word", "likelihood"]].to_csv(destination, index=False)


df_words = pd.read_csv(r"wordle_solver\datasets\unigram_freq.csv")

df_5letter = df_words[df_words["word"].str.len() == 5].copy(deep=True)
save_words_with_likelihood(
     df_5letter, r"wordle_solver\datasets\5letter_words.csv")

df_5letter_top5000 = df_5letter.head(5000).copy(deep=True)
save_words_with_likelihood(
    df_5letter_top5000, r"wordle_solver\datasets\5letter_words_top5000.csv")
