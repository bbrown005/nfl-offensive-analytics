import nflreadpy
import polars as pl

pbp = nflreadpy.load_pbp([2024])

print(type(pbp))
print(pbp.shape)
print(pbp.head())
print(pbp.columns)
print(pbp.schema)

columns = [
    "game_id",
    "play_id",
    "posteam",
    "fixed_drive",
    "play_type",
    "yards_gained",
    "drive_start_yard_line",
    "drive_play_count",
    "fixed_drive_result",
]

subset = pbp.select(columns)

print(subset.head(20))

missing_possession = pbp.filter(
    pbp["posteam"].is_null()
)

print(
    missing_possession.select(
        ["game_id", "play_id", "play_type", "desc", "posteam"]
    ).head(10)
)

drive_counts = (
    pbp
    .filter(pl.col("fixed_drive").is_not_null())
    .group_by(["game_id", "fixed_drive"])
    .agg([
        pl.len().alias("row_count"),
        pl.col("drive_play_count").drop_nulls().first().alias("drive_play_count"),
    ])
    .sort(["game_id", "fixed_drive"])
)

print(drive_counts.head(15))
discrepancies = drive_counts.filter(
    pl.col("row_count") != pl.col("drive_play_count")
)

print(discrepancies.head(15))
print("Drives with different counts:", discrepancies.height)

drive_1 = pbp.filter(
    (pl.col("game_id") == "2024_01_ARI_BUF")
    & (pl.col("fixed_drive") == 1)
)

print(
    drive_1.select([
        "play_id",
        "play_type",
        "yards_gained",
        "drive_play_count",
        "desc",
    ]).sort("play_id")
)

play_types = (
    pbp
    .group_by("play_type")
    .agg(
        pl.len().alias("count")
    )
    .sort("count", descending=True)
)

print(play_types)