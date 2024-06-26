import {
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  Transition,
} from "@headlessui/react";
import { CheckIcon, ChevronDownIcon } from "@heroicons/react/20/solid";
import React, { useState } from "react";

const statsOptions = [
  "POINTS",
  "REBOUNDS",
  "ASSISTS",
  "3PT",
  "3PTA",
  "FG",
  "FGA",
  "STEALS",
  "BLOCKS",
  "STOCKS",
  "PRA",
  "PTS + REBOUNDS",
  "POINTS + ASSISTS",
  "TURNOVERS",
];

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

export default function StatDropdown({ selectedStat, setSelectedStat }) {
  const [localSelectedStat, setLocalSelectedStat] = useState(selectedStat);

  const handleStatChange = (stat) => {
    setLocalSelectedStat(stat);
    setSelectedStat(stat);
  };

  return (
    <Menu as="div" className="relative inline-block text-left">
      <div>
        <MenuButton className="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-2 py-1 text-base font-normal text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 h-12">
          <span className="self-center">{localSelectedStat}</span>
          <ChevronDownIcon
            className="-mr-1 h-5 w-5 text-gray-400 self-center"
            aria-hidden="true"
          />
        </MenuButton>
      </div>

      <Transition
        as={React.Fragment}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <MenuItems className="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
          <div className="py-1">
            {statsOptions.map((stat) => (
              <MenuItem key={stat} as="div">
                {({ active }) => (
                  <button
                    onClick={() => handleStatChange(stat)}
                    className={classNames(
                      active ? "bg-gray-100 text-gray-900" : "text-gray-700",
                      "block px-4 py-2 text-sm w-full text-left"
                    )}
                  >
                    {stat}
                    {localSelectedStat === stat && (
                      <CheckIcon
                        className="h-5 w-5 inline ml-2 text-indigo-600"
                        aria-hidden="true"
                      />
                    )}
                  </button>
                )}
              </MenuItem>
            ))}
          </div>
        </MenuItems>
      </Transition>
    </Menu>
  );
}
