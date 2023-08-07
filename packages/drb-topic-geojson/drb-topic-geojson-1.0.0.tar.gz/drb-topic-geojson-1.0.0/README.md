# GeoJSON DRB topic

The `drb-topic-geojson` is a DRB plugin declaring a topic about
[GeoJSON](https://geojson.org/) data.

## Installation
```shell
pip install drb-topic-geojson
```

## GeoJSON topic
This section references the topic defined in this DRB plugin.

```mermaid
graph BT
    subgraph drb-driver-json 
        A([JSON<br/>c6f7d210-4df0-11ec-81d3-0242ac130003])
    end
    B([GeoJSON<br>d8c867e8-7185-4a82-adbe-a5f2a5ef63b6]) --> A
```