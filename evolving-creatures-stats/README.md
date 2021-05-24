# evolving-creatures

## Concepts and Ideas:

- Height map
- Moving speed
- Sensors
- Species
- altruism: sacrifice

- Neuronal network

## Important implemented concepts

*Evolution.py* 

1. There will always be a certain unfairness, since some creatures take turns first in a single frame, this is unavoidable.
Therefore exection order is randomized and a creature first in list does not benefit from always being the first to eat food etc.


## Open Questions

1. Do all creatures see the same distance?
2. Two creatures only interact with each other when strictly adjacent?
3. Creature eats food when standing on top of it?
4. Eating food takes one frame or does it slowly eat of the food?
5. When does the food regrow?
6. Where do the children spawn?
7. Do we have periodic boundaries?

## Issues

1. Periodic boundaries do not work for vision
2. Vision seems buggy