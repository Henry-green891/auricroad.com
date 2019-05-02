ENVIRONMENT_CHOICES = (
    ("", ""),
    ("mountains", "Mountains"),
    ("desert_riad", "Desert Riad"),
    ("beach", "Beach"),
    ("desert_ranch", "Desert Ranch"),
    ("vineyard", "Vineyard"),
)

FONT_CHOICES = (("a", "a"), ("b", "b"), ("c", "c"), ("d", "d"), ("e", "e"), ("f", "f"))

FONT_SIZE_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7))

ACCENT_BAR_CHOICES = (("vertical", "vertical"), ("horizontal", "horizontal"))

LAYOUT_CHOICES = (("image_first", "Image First"), ("image_second", "Image Second"))

IMAGE_GROUP_LAYOUTS = (
    ("half_width", "Half Width (Pick 2 Images)"),
    ("half_two_quarter", "One Half Width, Two Quarter Width (Pick 3 Images)"),
    (
        "double_height_half_right",
        "Two Quarters and Half Width Left, Double Height Half Right (Pick 4 Images)",
    ),
    (
        "double_height_half_left",
        "Double Height Half Left, Two Quarters and Half Width Right (Pick 4 Images)",
    ),
)
