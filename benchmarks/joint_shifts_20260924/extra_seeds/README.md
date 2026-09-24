# Additional joint-shift seeds

This extension adds seeds **13712** and **13713** to each frozen J1/J2/J3
selection, for six more 100-epoch models. Seed 13711 and its verified results
remain in the original run. The parent protocol SHA-256 is recorded in
`protocol.json`; audio selections, preprocessing, training hyperparameters,
final-epoch checkpoint rule, and MSE/Mahalanobis scoring stay fixed.

On the H100, this directory is copied to a separate run folder. Its `folds`
and `deps` entries link to the original run to reuse the pinned baseline code
and dependencies without duplicating data. `queue_extra.sh` audits each
selected dataset once, trains the six models sequentially, evaluates each
fixed test after training, and writes `queue.exit`. A prior checkpoint is
never overwritten; a successful partial queue can be resumed.

To shorten the H100 run while respecting the host's 31-GiB RAM limit,
`queue_helper.sh` can run J2/13712 then J3/13712 alongside the main queue.
It must begin while the main queue is still on J1, and finish each claimed
job before the main queue reaches it. The main queue then sees their success
receipts and skips them; do not start a third concurrent trainer.

No new scores or variability claims are added to the paper until the six
file-score tables and model hashes have been returned and independently
verified against the frozen selections.
