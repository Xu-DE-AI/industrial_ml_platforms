# Lineage lab

Track:

```text
raw reservoir
      |
      v
validated silver
      |
      v
gold features
      |
      v
training run
      |
      v
registered model
      |
      v
production prediction
```

Use OpenLineage/Marquez when you want a full local lineage server.

Interview question:

> If a model suddenly degrades, how do you identify which upstream data
> transformation changed?

Answer should involve lineage + dataset version + model version + run metadata.
