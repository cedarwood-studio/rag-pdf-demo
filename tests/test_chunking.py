from ragdemo.chunking import chunk_pages
from ragdemo.pdf import Line, Page, read_pdf


def test_chunks_keep_the_page_they_came_from(sample_pdf):
    chunks = chunk_pages(read_pdf(sample_pdf), "heading")
    by_page = {c.page: c for c in chunks}
    assert sorted(by_page) == [1, 2, 3]
    assert "thirty days" in by_page[1].text
    assert "citric acid" in by_page[2].text
    assert "three years" in by_page[3].text


def test_heading_is_detected_and_stored(sample_pdf):
    chunks = chunk_pages(read_pdf(sample_pdf), "heading")
    assert [c.heading for c in chunks] == ["1. Returns", "2. Descaling", "3. Warranty"]
    assert chunks[1].embed_text("Kettle Guide").startswith("Kettle Guide\n2. Descaling\n")


def test_running_header_is_removed_by_heading_chunker_only(sample_pdf):
    pages = read_pdf(sample_pdf)
    assert all("Kettle Guide" not in c.text for c in chunk_pages(pages, "heading"))
    assert all("Kettle Guide" in c.text for c in chunk_pages(pages, "fixed"))


def test_no_chunk_crosses_a_page_and_long_sections_split():
    body = [Line(text=f"Sentence number {i} about the same topic, long enough to matter.", size=11, bold=False) for i in range(40)]
    pages = [
        Page(number=7, lines=[Line("2.1 Long Section", 11, True)] + body),
        Page(number=8, lines=body[:5]),
    ]
    chunks = chunk_pages(pages, "heading", max_chars=600)
    assert len([c for c in chunks if c.page == 7]) > 1
    assert all(len(c.text) <= 700 for c in chunks)
    assert {c.page for c in chunks} == {7, 8}
    # The section carries over to the next page until a new heading appears.
    assert all(c.heading == "2.1 Long Section" for c in chunks)


def test_nested_headings_form_a_path():
    pages = [
        Page(number=1, lines=[
            Line("3. Handling an Incident", 12, True),
            Line("The response process has several phases. " * 8, 11, False),
            Line("3.1 Preparation", 11, True),
            Line("Preparation means having tools and people ready. " * 8, 11, False),
            Line("Table 3-1. Not a heading", 11, True),
        ])
    ]
    chunks = chunk_pages(pages, "heading")
    assert [c.heading for c in chunks] == ["3. Handling an Incident", "3. Handling an Incident > 3.1 Preparation"]


def test_unnumbered_front_matter_heading_does_not_stick_to_later_sections():
    filler = "Plain body text that fills the block so that it can stand alone. " * 5
    pages = [
        Page(number=1, lines=[Line("Errata", 14, True), Line(filler, 11, False)]),
        Page(number=2, lines=[Line("3.5 Plan Testing", 11, True), Line(filler, 11, False)]),
    ]
    assert [c.heading for c in chunk_pages(pages, "heading")] == ["Errata", "3.5 Plan Testing"]
