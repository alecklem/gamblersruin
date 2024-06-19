import React from "react";
import "../styles/RestDays.css";

const RestDays = ({ gameDates, restDays }) => {
  const getRestDayText = (days) => {
    if (days === "B2B") return "B2B";
    return days;
  };

  const getRestDayClass = (days) => {
    if (days === "B2B") return "b2b";
    if (days === "1 day") return "one-day";
    return "multi-day";
  };

  return (
    <div className="rest-days-container">
      {gameDates.map((date, index) => (
        <React.Fragment key={index}>
          <span className="game-date">{date}</span>
          {index < restDays.length && (
            <>
              <span className="rest-arrow">
                <span
                  className={`rest-days-text ${getRestDayClass(
                    restDays[index]
                  )}`}
                >
                  {getRestDayText(restDays[index])}
                </span>
                &rarr;
              </span>
            </>
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

export default RestDays;
