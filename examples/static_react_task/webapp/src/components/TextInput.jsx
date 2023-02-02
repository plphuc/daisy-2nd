const TextInput = ({ label, name, onChange, placeholder, error }) => {
  const handleChange = (e) => {
    onChange?.(e.target.value);
  };

  return (
    <div className="input-field">
      <label htmlFor={name}>{label}</label>
      <textarea
        rows="4"
        id={name}
        name={name}
        onChange={handleChange}
        placeholder={placeholder}
        style={{ width: "100%", resize: "none" }}
      />
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default TextInput;
