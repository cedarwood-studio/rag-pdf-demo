"""An interrupted ingest must not be mistaken for a finished one."""


def test_collection_is_complete_only_after_it_is_marked(pipeline):
    store = pipeline.retriever.store
    assert store.count("test") == 3  # the fixture stored chunks without finishing an ingest
    assert store.is_complete("test") is False
    store.mark_complete("test")
    store.mark_complete("test")  # marking twice is harmless
    assert store.is_complete("test") is True
    assert store.is_complete("another") is False


def test_deleting_a_collection_clears_the_mark(pipeline):
    store = pipeline.retriever.store
    store.add("scratch", [("a.pdf", "A", 1, "", "some text", [0.0] * store.dim)])
    store.mark_complete("scratch")
    store.delete_collection("scratch")
    assert store.count("scratch") == 0
    assert store.is_complete("scratch") is False
