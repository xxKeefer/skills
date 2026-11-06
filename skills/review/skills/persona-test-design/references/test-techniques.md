# Test techniques by code shape

   - a validated or numeric input → partitions + boundaries;
   - several conditions deciding one outcome → decision table;
   - a status enum, lifecycle or wizard → state transitions, **including invalid ones**;
   - two or more independent dimensions the code branches on → pairwise;
   - anything a user does over time → Zero/One/Many, CRUD with the permission off, interruptions (double-submit, navigate away mid-mutation, session expiry, account switch).
