from klassify.src.word_processor import WordProcessor
from klassify.src.tables import Document

initial_document_1 = Document(title="Test title 1", base_path="/test-1", content="This is a test document - one")
initial_document_2 = Document(title="Test title 2", base_path="/test-2", content="This is a test document - two")
initial_document_3 = Document(title="Test title 3", base_path="/test-3", content="This is a test document - three")

PROCESSOR = WordProcessor([
    initial_document_1,
    initial_document_2,
    initial_document_3,
])

new_document = Document(title="Self assessment deadlines 3", base_path="/self-assessment-3", html="<strong>PAY NOW 3</strong>", content="This has a different content - four")

def test_tokenize():
    tokenized_content = PROCESSOR.tokenize(initial_document_1)
    assert tokenized_content == ['This', 'is', 'a', 'test', 'document', "-", 'one']

def test_make_vocabulary():
    # without document
    assert PROCESSOR.make_vocabulary() == ['test', 'one', 'test', 'two', 'test', 'three']

    # with document
    assert PROCESSOR.make_vocabulary(new_document) ==  ['differ', 'content', 'four']

def test_bag_of_words():
    # This is built against the processor vocabulary.
    # The vocabulary is the sum of all the different terms in all the documents provided at instantiation.
    assert PROCESSOR.bag_of_words(initial_document_3) == {'one': False, 'test': True, 'three': True, 'two': False}

    assert PROCESSOR.bag_of_words(new_document) == {'one': False, 'test': False, 'three': False, 'two': False}

def test_process():
    # What will be filtered out:
    # - Single letter words
    # - Stop words
    # - Long words
    # Additionally, remaining words will be stemmed.
    document_with_unfiltered_content = Document(title="Test", base_path="/test",
        content=" within https .mb , a b c reallylongwordthatshouldbefilteredout cloudy regular words should be stemmed in this process"
    )

    tokenized_content = PROCESSOR.tokenize(document_with_unfiltered_content)

    assert PROCESSOR.process(tokenized_content) == ['cloudi', 'regular', 'word', 'stem', 'process']
