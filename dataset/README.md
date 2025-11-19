# Inner Harbor Dataset 📊  
### Physiological & Dialogue Data for Empathetic AI with HSP Users

---

## 1. Overview

This folder documents the datasets used in the **Inner Harbor** project, an empathetic AI companion for Highly Sensitive People (HSPs).

> 🔹 **Important:**  
> The **full datasets are hosted on Hugging Face** for version control and easier downloading.  

---

## 2. Hugging Face Datasets

You can find the full datasets here:

- **Main mixed dialogue dataset (for model fine-tuning)**  
  👉 `christinashihan/empathy_conciseediting`  
  Example usage:

  ```python
  from datasets import load_dataset

  ds = load_dataset("christinashihan/empathy_conciseediting")
  print(ds)

3. Sample Files in This Folder

To help readers quickly inspect the data format, this folder may include:

sample_hsp_data.json
A small sample of the instruction-style training data used to fine-tune the empathetic chatbot.

Typical record structure:
  ```
{
  "instruction": "User describes a situation where their emotions are overwhelmed.",
  "input": "Additional context about the user's day or environment (optional).",
  "output": "An empathetic, detailed, and emotionally supportive response from the AI."
}
  ```

The full dataset on Hugging Face follows the same schema but contains many more examples.

4. Data Sources & Collection

Physiological data are collected from wearable sensors (heart rate, HRV, GSR, temperature, breath rate, etc.) via Arduino and an integrated biosensor module.

Dialogue data are constructed from:

Simulated counseling-style conversations

HSP-specific emotional scenarios

Curated empathetic responses enriched with emojis for warmth

All data used for training or demonstration in this project are de-identified.

5. Ethics & Usage

The dataset is intended for research and educational purposes only.

It is not designed for clinical diagnosis or medical decision-making.

When reusing the dataset, please:

Respect the original context and purpose

Avoid any attempts at re-identification

Provide proper attribution to the author: Shihan Zhang (christinashihan)

Please refer to the Hugging Face dataset card for more detailed licensing and ethical notes.

6. How This Dataset Is Used in the Project

Used to fine-tune an empathetic chatbot model deployed in the Hugging Face Space
👉 christinashihan/Your_instantAIfriend

Provides domain-specific emotional patterns for HSPs, leading to:

More context-aware responses

Better emotional validation

Warmer, human-like interaction in stressful or overwhelming situations

For the full technical pipeline, see the main README.md
 in this repository.
