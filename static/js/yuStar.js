// star.js
function yuStar(p) {
	j('.medstar1').raty({
		path: p,
    readOnly: true,
    size: 16,
    space: false,
    score: 1,
	});
	j('.medstar2').raty({
		path: p,
    readOnly: true,
    size: 16,
    space: false,
    score: 2,
	});
	j('.medstar3').raty({
		path: p,
    readOnly: true,
    size: 16,
    space: false,
    score: 3,
	});
	j('.medstar4').raty({
		path: p,
    readOnly: true,
    size: 16,
    space: false,
    score: 4,
	});
	j('.medstar5').raty({
		path: p,
    readOnly: true,
    size: 16,
    space: false,
    score: 5,
	});
};