//React function
import DragNDropPanel from "./DragNDropPanel.jsx";
import TextInput from "./TextInput.jsx";
const Form = ({ taskData, submit }) => {
  const submitButtonStyles = {
    border: "2px solid grey",
    borderRadius: "12px",
    padding: "15px 32px",
    textAlign: "center",
    textDecoration: "none",
    display: "inline-block",
    fontSize: "16px",
    margin: "4px 2px",
    cursor: "pointer",
    backgroundColor: "rgb(255, 192, 0)",
  };
  const onSubmit = (e) => {
    e.preventDefault();
    const data = new FormData(e.target);

    let jsonObject = {};

    //loop through the data
    for (let pair of data.entries()) {
      if (pair[0] !== "right-panel" && pair[0] !== "left-panel") {
        jsonObject[pair[0]] = pair[1];
      } else if (pair[0] === "left-panel" || pair[0] === "right-panel") {
        jsonObject[pair[0]] = pair[1].split(",");
      }
    }

    submit(jsonObject);
  };

  return (
    <form onSubmit={onSubmit}>
      <p>
        A machine learning algorithm classifies the following entities as the
        same class. Drag-and-drop and add more entities of the <b>same class</b>{" "}
        from the right until all the entities on the right is in a different
        class.
      </p>
      <DragNDropPanel taskData={taskData} />

      <TextInput
        label={
          "In your opinion, what are the reasons the entities on the left are grouped in the same class? How did you obtain this knowledge?"
        }
        name={"opinion"}
        value={""}
        placeholder={"Write your opinion here"}
      />
      <TextInput
        label={
          "If you have any comments or feedback about our task, please write it below."
        }
        name={"comment"}
        value={""}
        placeholder={"Write your comment here"}
      />
      <input type="submit" style={submitButtonStyles} value="Submit" />
    </form>
  );
};

export default Form;
