// star.js
function yuStar(p) {
	jQuery('.medstar0').raty({
		path: p,
    readOnly: true,
    space: false,
    score: 0,
	});
	jQuery('.medstar1').raty({
		path: p,
    readOnly: true,
    space: false,
    score: 1,
	});
	jQuery('.medstar2').raty({
		path: p,
    readOnly: true,
    space: false,
    score: 2,
	});
	jQuery('.medstar3').raty({
		path: p,
    readOnly: true,
    space: false,
    score: 3,
	});
	jQuery('.medstar4').raty({
		path: p,
    readOnly: true,
    space: false,
    score: 4,
	});
	jQuery('.medstar5').raty({
		path: p,
    readOnly: true,
    space: false,
    score: 5,
	});
};