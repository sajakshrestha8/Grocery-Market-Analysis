import React, { useState, useEffect } from "react";
import axios from "axios";

const AnalysisResults = () => {
  const [results, setResults] = useState({
    associated_itemsets: [],
    frequent_itemsets: [],
    rules: [],
  });

  useEffect(() => {
    axios
      .get("/results") // Adjust the URL if necessary
      .then((response) => {
        setResults(response.data || {}); // Ensure that data is correctly set
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
        alert(
          "An error occurred while fetching the results. Please try again. Error: " +
            error.message
        );
      });
  }, []);

  const { associated_itemsets, frequent_itemsets, rules } = results;

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Market Basket Analysis Results</h1>

      {/* Display associated itemsets */}
      <div className="mb-4">
        <h2>Associated Itemsets</h2>
        {associated_itemsets.length === 0 ? (
          <div className="alert alert-info" role="alert">
            No associated itemsets found based on the current analysis.
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>Antecedent</th>
                  <th>Consequent</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                {associated_itemsets.map((itemset, index) => (
                  <tr key={index}>
                    <td>{itemset.antecedent.join(", ")}</td>
                    <td>{itemset.consequent.join(", ")}</td>
                    <td>{itemset.confidence.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Display frequent itemsets */}
      <div className="mb-4">
        <h2>Frequent Itemsets</h2>
        {frequent_itemsets.length === 0 ? (
          <div className="alert alert-info" role="alert">
            No frequent itemsets found based on the current analysis.
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>Itemset</th>
                </tr>
              </thead>
              <tbody>
                {frequent_itemsets.map((itemset, index) => (
                  <tr key={index}>
                    <td>{itemset.join(", ")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Display rules */}
      <div>
        <h2>Rules</h2>
        {rules.length === 0 ? (
          <div className="alert alert-info" role="alert">
            No rules found based on the current analysis.
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>Antecedent</th>
                  <th>Consequent</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                {rules.map((rule, index) => (
                  <tr key={index}>
                    <td>{rule.antecedent.join(", ")}</td>
                    <td>{rule.consequent.join(", ")}</td>
                    <td>{rule.confidence.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisResults;
