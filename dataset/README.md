# Inner Harbor Dataset 📊  
### Physiological & Dialogue Data for Empathetic AI with HSP Users

---

## 1. Overview

This folder documents the datasets used in the **Inner Harbor** project, an empathetic AI companion for Highly Sensitive People (HSPs).

> 🔹 **Important:**  
> The **full datasets are hosted on Hugging Face** for version control and easier downloading.  
> This GitHub repo only contains **small samples and documentation**, so that reviewers can quickly understand the data structure.

---

## 2. Hugging Face Datasets

You can find the full datasets here:

- **Main mixed dialogue dataset (for model fine-tuning)**  
  👉 `christinashihan/HSP_mixdataset_transformers`  
  Example usage:

  ```python
  from datasets import load_dataset

  ds = load_dataset("christinashihan/empathy_conciseediting")
  print(ds)
