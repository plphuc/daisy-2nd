import { useState, useCallback } from "react";
import { useDrop } from "react-dnd";
import { DraggableComponent } from "./Draggable.jsx";
const initialStyles = {
  color: "white",
  textAlign: "center",
  fontSize: "1rem",
  lineHeight: "normal",
};

const DroppableComponent = ({
  id,
  onItemMoved,
  accept,
  maxItems = 2,
  targetType,
  title,
  titleStyles,
  initialItems = [],
  draggableStyles,
  style,
  ...props
}) => {
  const [items, setItems] = useState(initialItems);

  const appendNewItems = useCallback((newItems) => {
    if (
      items?.filter((item) => item.id === newItems.id).length > 0 ||
      !newItems.length
    )
      return;
    setItems((cur) => [
      ...cur,
      ...newItems.map(({ id, name }) => ({ id, name })),
    ]);
  }, []);

  const removeItem = (id) => {
    if (items?.filter((item) => item.id === id).length === 0) return;
    setItems((cur) => cur?.filter((item) => item.id !== id) || []);
  };

  // the drop handler
  const onDrop = (item, dropTargetMonitor) => {
    appendNewItems([item]);
    // Return the drop result so that the source can be updated
    return { from: item.from, to: id, id: item.id, len: items.length };
  };

  const [{ canDrop, isOver }, dropRef] = useDrop(
    () => ({
      accept,
      drop: onDrop,
      // canDrop if the number of items is less than maxItems
      // or if maxItems is not specified
      canDrop: (item, dropTargetMonitor) =>
        maxItems ? items.length < maxItems : true,
      collect: (dropTargetMonitor) => {
        const dropResult = dropTargetMonitor.getDropResult();

        // If the drop target is the same as the source,
        // then we don't want to remove the item
        if (
          dropTargetMonitor.didDrop() &&
          dropResult &&
          dropResult.from === id
        ) {
          removeItem(dropResult.id);

          if (onItemMoved) {
            const newItems = onItemMoved(items.length, dropResult);
            if (newItems) {
              // If the parent component wants to update the items, then do so
              // This is useful when the parent component wants to update the
              // items based on the drop result
              // For example, if the parent component wants to update the items
              // based on the drop result, then it can do so by returning the
              // new items from the onItemMoved callback
              appendNewItems(newItems);
            }
          }
        }

        return {
          isOver: !!dropTargetMonitor.isOver(),
          canDrop: !!dropTargetMonitor.canDrop(),
        };
      },
    }),
    [items, removeItem, id]
  );

  // Change the background color based on whether the item is active
  const isActive = canDrop && isOver;
  let opacity = 1;
  let border = "3px solid rgba(237, 231, 225, 0.8)";
  if (isActive) {
    opacity = 0.3;
    border = "3px dotted rgba(237, 231, 225, 0.8)";
  } else if (canDrop) {
    opacity = 0.75;
    border = "3px dotted rgba(237, 231, 225, 0.8)";
  }

  const titleDefaultStyles = {
    width: "100%",
    padding: "20px 0px ",
    userSelect: "none",
  };

  return (
    <div
      data-id={"drop-" + id}
      ref={dropRef}
      style={{ ...initialStyles, ...style, opacity, border }}
      {...props}
    >
      <div style={{ ...titleDefaultStyles, ...titleStyles }}>{title}</div>
      <input type="hidden" name={id} value={items.map((item) => item.id)} />
      {isActive ? (
        <div style={{ position: "absolute", top: ".5em", textAlign: "center" }}>
          Release
        </div>
      ) : (
        canDrop && (
          <div
            style={{ position: "absolute", top: ".5em", textAlign: "center" }}
          >
            Here
          </div>
        )
      )}
      {items.map(({ id: itemId, name }, index) => (
        <DraggableComponent
          key={id + itemId}
          type={targetType}
          from={id}
          id={itemId}
          name={name}
          style={draggableStyles}
        />
      ))}
    </div>
  );
};

export default DroppableComponent;
