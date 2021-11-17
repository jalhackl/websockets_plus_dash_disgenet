


(function() {
    class MyTitle extends HTMLElement {
      constructor() {
        super();
  
        this.attachShadow({ mode: 'open' });
       


        this.shadowRoot.innerHTML = `
          <style>
            h1 {
              font-size: 2.5rem;
              color: hotpink;
              font-family: monospace;
              text-align: center;
              text-decoration: pink solid underline;
              text-decoration-skip: ink;
            }
          </style>
          <button type="button" id="send" class="btn btn-success">ADD</button>
          <h1>Hello Alligator!</h1>
        `;
      }
    }
  
    window.customElements.define('my-title', MyTitle);
  })();
