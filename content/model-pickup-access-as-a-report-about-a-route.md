# Model Pickup Access as a Report About a Route

A wheelchair ride request can include a precise street address and still leave a crucial question unanswered. Can the rider reach the place where the vehicle will load? One entrance might have a step-free path to a loading bay. A different entrance at the same address might lead to stairs. A temporary closure can also make yesterday’s answer stale.

It uses fictional records.

## Model the path between two places

Store an entrance ID and a loading zone ID together. A report describes the path between those two points. Give the report a source, such as a facility contact or a site observation, and store when the information was observed and when it should be checked again. A new loading bay requires its own evidence, even if the street address stays the same.

The U.S. Access Board’s [passenger loading zone guide](https://www.access-board.gov/ada/guides/chapter-5-passenger-loading-zones/) distinguishes the vehicle pull-up space, the access aisle and the connected accessible route. That distinction is a useful starting point for a data model. The example below tracks observations for a ride request. It makes no compliance determination.

## Filter observations for the intended pickup

The function expects validated reports. Timestamps are numeric, in the same time unit, and report status is either `step_free_reported` or `blocked`. The server sets the time of the check. A report can be considered only when someone observed it by that time and it is still valid for the planned pickup.

```js
function pickupAccess(trip, reports) {
  const observations = reports.filter((report) =>
    report.entranceId === trip.entranceId &&
    report.loadingZoneId === trip.loadingZoneId &&
    report.observedAt <= trip.checkedAt &&
    trip.checkedAt <= trip.pickupAt &&
    trip.pickupAt < report.validUntil
  );

  const outcomes = new Set(observations.map(({ status }) => status));
  if (outcomes.size !== 1) return 'needs_check';
  return outcomes.has('blocked') ? 'barrier_reported' : 'report_available';
}
```

A report for a different entrance, a different loading bay or an expired validity window stays out of the decision. Two current reports with opposing outcomes return `needs_check`. That avoids silently picking whichever report happened to arrive last. An active barrier report can go to a person to follow up. A step-free report is one piece of information for planning and still leaves the vehicle and boarding arrangement to confirm.

## Tell the user what the system knows

- For `needs_check`, show “Confirm the route to this pickup point.”
- For `barrier_reported`, show “A barrier was reported. Check for an alternate pickup point.”
- For `report_available`, show “Step-free route reported,” followed by the source and the date checked.

If the entrance, loading point or pickup time changes, rerun the check. Use the same calculation in the staff view and the public form so both screens agree on which details still need confirmation.
