vocabulary = ["tax", "expenses", "benefits", "director", "hmrc"]
document_bow = ["tax", "benefits", "hmrc"]

# After vectorization against Vocabulary:
machine_readable_content = {
  tax: True
  expenses: False
  benefits: True
  director: False
  hmrc: True
}
