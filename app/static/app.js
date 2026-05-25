// Global State
let categoriesData = [];
let activeCategoryKey = 'length';

// DOM Elements
const categoryTabs = document.getElementById('categoryTabs');
const inputValue = document.getElementById('inputValue');
const fromUnit = document.getElementById('fromUnit');
const toUnit = document.getElementById('toUnit');
const resultValue = document.getElementById('resultValue');
const resultSymbol = document.getElementById('resultSymbol');
const resultFormula = document.getElementById('resultFormula');
const swapBtn = document.getElementById('swapBtn');
const copyBtn = document.getElementById('copyBtn');

// Init
window.addEventListener('DOMContentLoaded', async () => {
    await fetchCategories();
    setupEventListeners();
});

// Fetch supported categories and units from backend
async function fetchCategories() {
    try {
        const response = await fetch('/api/categories');
        if (!response.ok) throw new Error('Failed to load categories');
        categoriesData = await response.ok ? await response.json() : [];
        
        if (categoriesData.length > 0) {
            activeCategoryKey = categoriesData[0].key;
            renderCategories();
            populateUnits(activeCategoryKey);
            triggerConversion();
        }
    } catch (err) {
        console.error('Error fetching categories:', err);
        resultFormula.innerText = 'Error connecting to conversion service.';
    }
}

// Render tabs dynamically
function renderCategories() {
    categoryTabs.innerHTML = '';
    categoriesData.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = `category-tab ${cat.key === activeCategoryKey ? 'active' : ''}`;
        btn.setAttribute('role', 'tab');
        btn.setAttribute('aria-selected', cat.key === activeCategoryKey);
        btn.innerHTML = `
            <span class="tab-icon">${cat.icon}</span>
            <span class="tab-label">${cat.name}</span>
        `;
        
        btn.addEventListener('click', () => {
            if (activeCategoryKey !== cat.key) {
                activeCategoryKey = cat.key;
                
                // Update active state in UI
                document.querySelectorAll('.category-tab').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                populateUnits(activeCategoryKey);
                triggerConversion();
            }
        });
        
        categoryTabs.appendChild(btn);
    });
}

// Populate unit drop downs
function populateUnits(catKey) {
    const category = categoriesData.find(c => c.key === catKey);
    if (!category) return;
    
    fromUnit.innerHTML = '';
    toUnit.innerHTML = '';
    
    category.units.forEach(u => {
        const optFrom = document.createElement('option');
        optFrom.value = u.key;
        optFrom.innerText = `${u.name} (${u.symbol})`;
        
        const optTo = optFrom.cloneNode(true);
        
        fromUnit.appendChild(optFrom);
        toUnit.appendChild(optTo);
    });
    
    // Choose sensible defaults (first and second units)
    if (category.units.length > 1) {
        fromUnit.selectedIndex = 0;
        toUnit.selectedIndex = 1;
    }
}

// Perform calculation API request
async function triggerConversion() {
    const val = parseFloat(inputValue.value);
    if (isNaN(val)) {
        resultValue.innerText = '—';
        resultSymbol.innerText = '';
        resultFormula.innerText = 'Please enter a valid number';
        return;
    }
    
    const requestData = {
        category: activeCategoryKey,
        from_unit: fromUnit.value,
        to_unit: toUnit.value,
        value: val
    };
    
    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            const errorDetails = await response.json();
            throw new Error(errorDetails.detail || 'Conversion error');
        }
        
        const data = await response.json();
        
        // Find target unit symbol
        const cat = categoriesData.find(c => c.key === activeCategoryKey);
        const unit = cat?.units.find(u => u.key === toUnit.value);
        const symbol = unit ? unit.symbol : '';
        
        // Render
        resultValue.innerText = formatNumber(data.converted_value);
        resultSymbol.innerText = symbol;
        resultFormula.innerText = `Formula: ${data.formula}`;
    } catch (err) {
        console.error('Conversion API Error:', err);
        resultValue.innerText = 'Error';
        resultSymbol.innerText = '';
        resultFormula.innerText = err.message;
    }
}

// Formats result for crisp presentation
function formatNumber(num) {
    // If integer, return as is
    if (Number.isInteger(num)) return num.toString();
    
    // Otherwise limit decimals to 6, strip trailing zeros
    let formatted = num.toFixed(6);
    return parseFloat(formatted).toString();
}

// Setup listeners for user events
function setupEventListeners() {
    inputValue.addEventListener('input', debounce(triggerConversion, 150));
    fromUnit.addEventListener('change', triggerConversion);
    toUnit.addEventListener('change', triggerConversion);
    
    // Swap Units Action
    swapBtn.addEventListener('click', () => {
        const temp = fromUnit.value;
        fromUnit.value = toUnit.value;
        toUnit.value = temp;
        
        // Add rotation micro-animation
        const icon = swapBtn.querySelector('.swap-icon');
        icon.style.transform = icon.style.transform === 'rotate(180deg)' ? 'rotate(360deg)' : 'rotate(180deg)';
        
        triggerConversion();
    });
    
    // Copy result to clipboard
    copyBtn.addEventListener('click', () => {
        const text = `${inputValue.value} ${getSelectedUnitSymbol(fromUnit)} = ${resultValue.innerText} ${resultSymbol.innerText}`;
        navigator.clipboard.writeText(text).then(() => {
            copyBtn.classList.add('copied');
            const span = copyBtn.querySelector('span');
            span.innerText = 'Copied!';
            
            setTimeout(() => {
                copyBtn.classList.remove('copied');
                span.innerText = 'Copy Result';
            }, 2000);
        });
    });
}

function getSelectedUnitSymbol(selectElem) {
    const selectedText = selectElem.options[selectElem.selectedIndex]?.text || '';
    const match = selectedText.match(/\(([^)]+)\)/);
    return match ? match[1] : '';
}

// Simple debounce helper to prevent spamming backend on keystrokes
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
