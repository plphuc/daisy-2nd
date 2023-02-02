import { useDrag } from "react-dnd";
const initialStyles = {
  cursor: "move",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
};

export const DraggableComponent = ({
  id,
  name,
  from,
  type = "box",
  style,
  ...props
}) => {
  const [{ isDragging }, dragRef] = useDrag(() => ({
    type,
    item: { id, name, from },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
      handlerId: monitor.getHandlerId(),
    }),
  }));

  const opacity = isDragging ? 0.75 : 1;
  return (
    <div
      ref={dragRef}
      style={{ ...initialStyles, ...style, opacity }}
      {...props}
    >
      <span>{name}</span>
    </div>
  );
};
