import polars as pl


def filter_offensive_plays(pbp: pl.DataFrame) -> pl.DataFrame:
    """Return qualifying offensive plays."""
    return pbp.filter(
        pl.col("play_type").is_in(["run", "pass"])
        & (pl.col("qb_kneel").fill_null(0) != 1)
        & (pl.col("qb_spike").fill_null(0) != 1)
        & (pl.col("two_point_attempt").fill_null(0) != 1)
    )