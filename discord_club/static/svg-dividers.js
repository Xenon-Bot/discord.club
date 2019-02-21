function createSVGDivicer(selector, color, reverse) {
    $(selector).html(`
        <svg style="width: 100%; height: 5vh;" class="bg-light" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
            <polygon fill="${color}" points="${reverse ? '0,100 0,0 100,0' : '0,100 100,0 100,100'}"></polygon>
        </svg>
    `);
}