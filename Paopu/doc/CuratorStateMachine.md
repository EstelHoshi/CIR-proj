stateDiagram-v2
    opened --> opened : approve
    opened --> closed : close_pull_request
    opened --> merged : merge_pull_request
    opened --> opened : request_changes
