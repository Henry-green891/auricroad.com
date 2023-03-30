ENVIRONMENT_CHOICES = (
    ("", ""),
    ("mountains", "Mountains"),
    ("desert_riad", "Desert Riad"),
    ("beach", "Beach"),
    ("desert_ranch", "Desert Ranch"),
    ("vineyard", "Vineyard"),
)

FONT_CHOICES = (("a", "a"), ("b", "b"), ("c", "c"), ("d", "d"), ("e", "e"), ("f", "f"))

FONT_STYLE_CHOICES = (
    ("normal", "normal"),
    ("italic", "italic"),
    ("oblique", "oblique"),
)

FONT_SIZE_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7))

ACCENT_BAR_CHOICES = (("vertical", "vertical"), ("horizontal", "horizontal"))

LAYOUT_CHOICES = (("image_first", "Image First"), ("image_second", "Image Second"))

X_POSITIONS = (("center", "center"), ("left", "left"), ("right", "right"))
Y_POSITIONS = (("top", "top"), ("center", "center"), ("bottom", "bottom"))

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
    ("one_third_two_thirds", "One 1/3 Image on left, One 2/3 Image (Pick 2 Images)"),
    ("two_thirds_one_third", "One 2/3 Image on left, One 1/3 Image (Pick 2 Images)"),
)

SOCIAL_TYPES = (
    ("instagram", "Instagram"),
    ("facebook", "Facebook"),
    ("twitter", "Twitter"),
    ("linkedin", "Linkedin"),
)

CUSTOM_TEXT_FUNCTIONS = (("phone", "Phone"), ("email", "Email"))

VIDEO_SOURCES = (("vimeo", "Vimeo"),)

PETITE_RESORTS = (
    ("", ""),
    ("korakia_events_form_link", "Korakia"),
    ("hotel_joaquin_events_form_link", "Hotel Joaquin"),
    ("lone_mountain_ranch_events_form_link", "Lone Mountain Ranch"),
    ("sonoma_events_form_link", "Sonoma Coast Villa"),
)

#CACHE_STRING = "public, max-age=600, must-revalidate"
