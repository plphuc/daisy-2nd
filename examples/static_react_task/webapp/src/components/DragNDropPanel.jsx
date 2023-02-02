import { useMemo } from "react";
import { HTML5Backend } from "react-dnd-html5-backend";
import { DndProvider } from "react-dnd";
import DroppableComponent from "./Droppable.jsx";

const PanelIds = {
  Left: "left-panel",
  Right: "right-panel",
};

const DragNDropPanel = ({ taskData }) => {
  const names = useMemo(() => taskData.entities.map((entity) => entity.name), [
    taskData.entities,
  ]);
  const left_panel = useMemo(
    () =>
      taskData.left_panel
        .map((entity) => entity.name)
        .map((d) => ({
          id: d,
          // and replace _ with space
          name: d.replace(/_/g, " "),
        })),
    [taskData.entities]
  );

  let data = names.map((d) => ({
    id: d,
    // and replace _ with space
    name: d.replace(/_/g, " "),
  }));

  const randomPop = (num) => {
    //validate if num is a number and larger than 0
    if (isNaN(num) || num <= 0) {
      return;
    }

    // random index between 0 and data.length - num
    const index = Math.floor(Math.random() * (data.length - num));
    const removedItems = data.splice(index, num);
    // filter out the removed items
    data = data.filter(({ id }) => !removedItems.map((d) => d.id).includes(id));

    return removedItems;
  };

  // function that is called when an item is
  // dropped on the right panel
  // return a list of items will be added to the right panel
  const onItemMoved = (itemsLength, _) => {
    // if item length larger than 10, return empty list
    if (itemsLength > 10) {
      return [];
    }

    return [...randomPop(1)];
  };

  const droppableStyles = {
    width: "45%",
    padding: "0px 0px 2em 0px ",
    display: "flex",
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "start",
    alignItems: "start",
    alignContent: "start",
    color: "black",
  };

  const draggableStyles = {
    width: "45%",
    marginLeft: "2.5%",
    // backgroundColor: "lightblue",
    borderRadius: "5px",
    border: "0.5px solid rgba(100, 100, 100, 0.8)",
    marginTop: ".5em",
    height: "3em",
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div
        style={{
          overflow: "hidden",
          display: "flex",
          justifyContent: "space-between",
          width: "100%",
        }}
      >
        <DroppableComponent
          id={PanelIds.Left}
          targetType={PanelIds.Right}
          initialItems={left_panel}
          accept={PanelIds.Left}
          style={droppableStyles}
          draggableStyles={draggableStyles}
          maxItems={null}
          title={
            <>
              These are in the{" "}
              <b style={{ color: "rgb(275,92,0)" }}>same class..</b>
            </>
          }
          titleStyles={{ backgroundColor: "rgb(255,192,0)" }}
        />

        <DroppableComponent
          id={PanelIds.Right}
          onItemMoved={onItemMoved}
          initialItems={randomPop(10)}
          targetType={PanelIds.Left}
          accept={PanelIds.Right}
          style={droppableStyles}
          maxItems={null}
          draggableStyles={draggableStyles}
          titleStyles={{ backgroundColor: "rgb(204,228,189)" }}
          title="Please add more entities from below to left."
        />
      </div>
    </DndProvider>
  );
};
export default DragNDropPanel;
