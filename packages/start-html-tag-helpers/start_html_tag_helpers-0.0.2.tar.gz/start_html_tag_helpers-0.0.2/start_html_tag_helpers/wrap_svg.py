from .filter_attrs import help_aria

from bs4 import BeautifulSoup, Tag


def wrap_svg(
    html_markup: str,
    css: str | None = None,
    outer_css: str | None = None,
    pre_text: str | None = None,
    pre_css: str | None = None,
    post_text: str | None = None,
    post_css: str | None = None,
    **kwargs,
) -> BeautifulSoup:
    """Supplement html fragment of `<svg>` icon with css classes and attributes, include parent/sibling `<span>`s when parameters dictate.

    Examples:
        >>> markup = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5"><path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" /></svg>'
        >>> res = wrap_svg(html_markup=markup, pre_text="Close menu", pre_css="sr-only", aria_hidden="true")
        >>> len(res.contents) == 2
        True
        >>> res.contents[0]
        <span class="sr-only">Close menu</span>
        >>> res.contents[1].attrs == {'xmlns': 'http://www.w3.org/2000/svg', 'viewbox': '0 0 20 20', 'fill': 'currentColor', 'class': ['w-5', 'h-5'], 'aria-hidden': 'true'}
        True

    Args:
        html_markup (str): The template that contains the `<svg>` tag converted into its html string format.
        css (str, optional): Previously defined CSS to add to the `<svg>` icon. Defaults to None.
        outer_css (str | None, optional): CSS to set in a to be created parent `<span>` of the `<svg>` icon. Defaults to None.
        pre_text (str | None, optional): Text to be included in a prior sibling`<span>` to the `<svg>` icon. Defaults to None.
        pre_css (str | None, optional): CSS to set in prior `<span>`. Defaults to None.
        post_text (str | None, optional): Text to be included in a succeeding sibling `<span>`  to the `<svg>` icon. Defaults to None.
        post_css (str | None, optional): CSS to set in succeeding `<span>`. Defaults to None.

    Returns:
        SafeString: Small HTML fragment visually representing an svg icon.
    """  # noqa: E501

    def add_span(
        soup: BeautifulSoup, txt: str | None = None, kls: str | None = None
    ) -> Tag | None:
        """Add a new `<span>` tag within an existing BeautifulSoup object and assign it
        a class attribute."""
        if txt:
            span = soup.new_tag("span")
            span.string = txt
            if kls:
                span["class"] = kls
            return span
        return None

    soup = BeautifulSoup(html_markup, "html.parser")
    icon = soup("svg")[0]
    if css:
        icon["class"] = css
    if aria_attrs := help_aria(kwargs):
        for k, v in aria_attrs.items():
            icon[k] = v
    # sibling spans of icon svg tag
    if pre := add_span(soup, pre_text, pre_css):
        icon.insert_before(pre)
    if post := add_span(soup, post_text, post_css):
        icon.insert_after(post)
    if outer_css:
        cover = soup.new_tag("span")
        cover["class"] = outer_css
        icon.wrap(cover)
    return soup
