# Feast exercise

Install Feast and initialize a local feature repository.

Exercises:

1. Define `well_id` as an entity.
2. Define historical features.
3. Materialize features to an online store.
4. Run point-in-time historical retrieval.
5. Request online features for one well.
6. Compare online and offline values.

The most important concept is:

**point-in-time correctness**

A training row at time `t` must only use information available at or before `t`.
