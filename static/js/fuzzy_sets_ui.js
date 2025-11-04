// Client-side UI for Fuzzy Sets adaptive form
(function(){
  const binaryOps = new Set([
    'Equality','Intersection','Union','Algebraic Product','Algebraic Sum',
    'Algebraic Difference','Bounded Sum','Bounded Difference','Cartesian Product','Composition'
  ]);
  const unaryOps = new Set(['Complement']);
  const scalarOps = new Set(['Power of Fuzzy Set','Multiplication by Crisp Number']);

  const hints = {
    'Complement': "Complement: computes μ'(x) = 1 − μ(x)",
    'Power of Fuzzy Set': "Power: raises membership to a power μ(x)^p (choose p)",
    'Multiplication by Crisp Number': "Multiply: scales membership by a crisp number k (choose k)",
    'Equality': "Equality: checks whether two fuzzy sets have equal membership values",
    'Intersection': "Intersection (min): μ_{A∩B}(x) = min(μ_A(x), μ_B(x))",
    'Union': "Union (max): μ_{A∪B}(x) = max(μ_A(x), μ_B(x))",
    'Algebraic Product': "Algebraic Product: μ_A(x) * μ_B(x)",
    'Algebraic Sum': "Algebraic Sum: A + B - A*B",
    'Algebraic Difference': "Algebraic Difference: A * (1 - B)",
    'Bounded Sum': "Bounded Sum: min(1, A + B)",
    'Bounded Difference': "Bounded Difference: max(0, A - B)",
    'Cartesian Product': "Cartesian Product: creates a relation matrix R(x,y)=min(μ_A(x), μ_B(y))",
    'Composition': "Composition: computes relation composition (Max–Min) between relations derived from sets"
  };

  function qs(sel){ return document.querySelector(sel); }

  document.addEventListener('DOMContentLoaded', ()=>{
    const opSelect = qs('#operation-select');
    const setARow = qs('#seta-row');
    const setBRow = qs('#setb-row');
    const scalarRow = qs('#scalar-row');
    const hintBox = qs('#operation-hint');
    const form = qs('form.form-area');
    const explainBtn = qs('button[name="explain"]');
    const computeBtn = qs('button[name="compute"]');
    const explanationLoading = qs('#explanation-loading');

    if(!opSelect || !form) return;

    function updateVisibility(){
      const op = opSelect.value || '';
      // Set A always visible
      setARow.style.display = 'block';

      // If no operation selected (default) or a binary operation, show Set B
      if(op === '' || binaryOps.has(op)){
        setBRow.style.display = 'block';
      } else {
        setBRow.style.display = 'none';
      }

      if(scalarOps.has(op)){
        scalarRow.style.display = 'flex';
      } else {
        scalarRow.style.display = 'none';
      }

      // If unary op (Complement) we only show Set A (already ensured)

      // update hint
      hintBox.textContent = hints[op] || '';
    }

    // initial state based on server-rendered operation value
    updateVisibility();

    opSelect.addEventListener('change', updateVisibility);

    // client-side validation on submit
    form.addEventListener('submit', (ev)=>{
      const op = opSelect.value || '';
      const setA = qs('textarea[name="setA"]').value.trim();
      const setB = qs('textarea[name="setB"]').value.trim();
      const scalarVal = qs('input[name="scalar"]').value.trim();

      // Set A must not be empty
      if(!setA){
        ev.preventDefault();
        alert('Please provide Set A.');
        qs('textarea[name="setA"]').focus();
        return;
      }

      // If binary op, Set B required
      if(binaryOps.has(op)){
        if(!setB){
          ev.preventDefault();
          alert('This operation requires Set B. Please provide Set B.');
          qs('textarea[name="setB"]').focus();
          return;
        }
      }

      // If scalar op, scalar must be valid number
      if(scalarOps.has(op)){
        if(!scalarVal || isNaN(Number(scalarVal))){
          ev.preventDefault();
          alert('Please provide a valid numeric scalar for this operation.');
          qs('input[name="scalar"]').focus();
          return;
        }
      }

      // allow submit to continue
    });

    // show loading for Explain button
    if(explainBtn){
      explainBtn.addEventListener('click', ()=>{
        if(explanationLoading) explanationLoading.style.display = 'inline';
      });
    }

  });
})();
