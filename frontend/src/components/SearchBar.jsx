import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const SearchBar = () => {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [definition, setDefinition] = useState("");
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);

  // Fetch Word Definition
  const fetchDefinition = async () => {
    if (query) {
      setLoading(true);
      try {
        const response = await fetch(`http://127.0.0.1:8000/define/?word=${query}`);
        const data = await response.json();
        if (data.definitions && data.definitions.length > 0) {
          setDefinition(data.definitions.join("\n"));
        } else {
          setDefinition("No definition found.");
        }
        setShowModal(true);
      } catch (error) {
        setDefinition("Error fetching definition.");
        setShowModal(true);
      }
      setLoading(false);
    }
  };

  // Handle Input Change
  const handleChange = async (e) => {
    const input = e.target.value;
    setQuery(input);

    if (input.length === 0) {
      setSuggestions([]);
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/suggest/?prefix=${input}`);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setSuggestions(data.suggestions || []);
    } catch (error) {
      console.error("Error fetching suggestions:", error);
      setSuggestions([]);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              placeholder="Search for a word..."
              value={query}
              onChange={handleChange}
            />
            <button className="btn btn-primary" onClick={fetchDefinition} disabled={loading}>
              {loading ? <span className="spinner-border spinner-border-sm"></span> : "Search"}
            </button>
          </div>

          {/* Suggestions Dropdown */}
          {suggestions.length > 0 && (
            <ul className="list-group mt-2">
              {suggestions.map((word, index) => (
                <li
                  key={index}
                  className="list-group-item list-group-item-action"
                  onClick={() => setQuery(word)}
                  style={{ cursor: "pointer" }}
                >
                  {word}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Bootstrap Modal for Definition */}
      {showModal && (
        <div className="modal fade show d-block" tabIndex="-1">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">{query}</h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
              </div>
              <div className="modal-body">
                <p>{definition}</p>
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
