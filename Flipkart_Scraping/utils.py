def get_format_link(link, old_value, new_value):
    new_link = link.replace(old_value, new_value)
    new_link = new_link.replace("q=70", "q=100")
    return new_link
