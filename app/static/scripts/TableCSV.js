export default class {
  /**
   * @param {HTMLTableElement} root The table element which will display the CSV data.
   */
  constructor(root) {
    this.root = root;
    console.log("I am constructed!");
  }

  /**
   *
   * @param {string[]} headerColumns List of headings to be used.
   */
  setHeader(headerColumns) {
    this.root.insertAdjacentHTML(
      "afterbegin",
      `
            <thead>
                <tr>
                ${headerColumns.map((text) => `<td>${text}</th>`).join("")}
                </tr>
            </thead>
        `
    );
  }

  /**
   *
   * @param {string[][]} data a 2D array of data to be used as the table body
   * @param {string[]} headerColumns List of headings to be used
   */
  update(data, headerColumns = []) {
    this.clear();
    this.setHeader(headerColumns);
    this.setBody(data);
  }

  /**
   *
   * @param {string[]} a 2D array of data to be used as the table body.
   */
  setBody(data) {
    const rowsHtml = data.map((row) => {
      return `
       <tr>
            ${row.map((text) => `<td>${text.substr(0, 21)}</td>`).join("")}
       </tr>
       `;
    });
    this.root.insertAdjacentHTML(
      "beforeend",
      `
        <tbody>
        ${rowsHtml.join("")}
        </tbody>
    `
    );
  }

  /**
   * Clears all contents of the table (incl. the header).
   */
  clear() {
    this.root.innerHTML = "";
  }
}
