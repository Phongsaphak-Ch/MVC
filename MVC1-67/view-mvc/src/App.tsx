import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [cowCode, setCowCode] = useState<string>(""); // To input cow ID
  const [msg, setMsg] = useState<string>(""); // To display message
  const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
  const [cowData, setCowData] = useState<any[]>([]); // To store cow data
  const [milk, setMilk] = useState<{ [key: string]: number }>({}); // To store milk data
  const [isLoading, setIsLoading] = useState<boolean>(false)

  const handleSubmit = async () => {
    try {
      setIsLoading(true)
      // Send a GET request with cow_id as a query parameter
      const response = await axios.get(`${apiUrl}/get_milk_production`, {
        params: { cow_id: cowCode },
      });


      setMsg(
        `Cow ID: ${response.data.cow_id}, Breed: ${response.data.breed}, Milk Type: ${response.data.milk_type}, Milk Produced: ${response.data.milk_production} liters`
      );
    } catch (error: any) {
      // Check if the error is from Axios and has a response
      if (error.response) {
        const errorDetails = error.response.data;

        if (Array.isArray(errorDetails)) {
          const formattedErrors = errorDetails
            .map(
              (err: any) => `${err.loc ? err.loc.join(" -> ") : ""}: ${err.msg}`
            )
            .join("\n");
          setMsg(`Error:\n${formattedErrors}`);
        } else if (errorDetails.detail) {
          console.log(errorDetails.detail);
          setMsg(`Error: ${JSON.stringify(errorDetails.detail)}`);
        } else {
          setMsg(`Error: ${JSON.stringify(errorDetails)}`);
        }
      } else if (error.request) {
        setMsg("Error: No response from the server. Please try again later.");
      } else {
        setMsg(`Error: ${error.message}`);
      }
      console.error("Error occurred:", error);
    }
    finally {
      setIsLoading(false)
    }
  };

  // useEffect to fetch cow data when the component mounts
  useEffect(() => {
    const fetchCowData = async () => {
      try {
        // Call the API to get cow data
        const response = await axios.get(`${apiUrl}/get_cow_data`);
        setCowData(response.data.data); // Set the cow data into state
        setMilk(response.data.milk);
        console.log(response.data.milk);
      } catch (error: any) {
        // Error handling
        if (error.response) {
          setMsg(`Error: ${error.response.data.message}`);
        } else if (error.request) {
          setMsg("Error: No response from the server. Please try again later.");
        } else {
          setMsg(`Error: ${error.message}`);
        }
      }
    };

    fetchCowData();
  }, [apiUrl, isLoading]);

  return (
    <>
      <div className="container">
        <div className="column-container">
          <div className="row-container">
            <p style={{ color: "black" }}>Cow code: </p>
            <input
              type="text"
              value={cowCode}
              onChange={(e) => setCowCode(e.target.value)}
              placeholder="Enter Cow ID"
            />
          </div>
          <button type="submit" onClick={handleSubmit}>
            Submit
          </button>
          {msg && <p style={{ color: "black" }}>Response Message: {msg}</p>}
        </div>
      </div>
      <div className="container">
        <h3 style={{ color: "black" }}>Total milk production</h3>
        <div className="milk-list">
          {Object.keys(milk).length > 0 ? (
            <ul>
              {Object.entries(milk).map(([milkType, amount], index) => (
                <li key={index}>
                  <strong>Milk Type:</strong> {milkType},{" "}
                  <strong>Amount Produced:</strong> {amount} liters
                </li>
              ))}
            </ul>
          ) : (
            <p>No milk data available.</p>
          )}
        </div>
      </div>
      <div className="container">
        <h3 style={{ color: "black" }}>Cow Data</h3>
        <div className="cow-list">
          {cowData.length > 0 ? (
            <ul>
              {cowData.map((cow, index) => (
                <li key={index}>
                  <strong>ID:</strong> {cow.cow_id}, <strong>Breed:</strong>{" "}
                  {cow.breed},<strong>Color:</strong> {cow.color},{" "}
                  <strong>Age:</strong> {cow.age_years} years, {cow.age_months}{" "}
                  months
                </li>
              ))}
            </ul>
          ) : (
            <p>No cow data available.</p>
          )}
        </div>
      </div>
    </>
  );
}

export default App;
