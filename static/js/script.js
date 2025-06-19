document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Script iniciado para pets!');

    const dog = document.getElementById('dog-walker');
    const cat = document.getElementById('cat-walker');
    const screenWidth = window.innerWidth;
    const speed = 2; // Velocidade de caminhada (pixels por frame)

    if (!dog) {
        console.error("Erro: Elemento 'dog-walker' não encontrado no HTML. Verifique o ID.");
        return;
    }
    if (!cat) {
        console.error("Erro: Elemento 'cat-walker' não encontrado no HTML. Verifique o ID.");
        return;
    }

    // --- Nova lógica para posicionar no rodapé ---
    const footer = document.querySelector('footer');
    let footerHeight = 0;
    let petsBottomPosition = 0;

    if (footer) {
        // Pega a altura do rodapé
        footerHeight = footer.offsetHeight;
        // Calcula a posição 'bottom' para os pets ficarem no rodapé
        // 'offsetHeight' inclui padding e borda. Se o pet tiver altura 70px,
        // e você quer ele centrado ou na parte de cima do rodapé, ajuste aqui.
        // Por exemplo, para eles ficarem no meio do rodapé:
        petsBottomPosition = (footerHeight - dog.offsetHeight) / 2;
        // Ou se você quiser eles "sentados" na linha de cima do rodapé:
        // petsBottomPosition = footerHeight - dog.offsetHeight;
        // Ou se você quiser eles um pouco acima do rodapé (20px de margem):
        petsBottomPosition = footerHeight + 20; // 20px acima da base do rodapé
        // **Experimente com este valor até encontrar a altura ideal para seus pets**

        console.log(`Rodapé encontrado. Altura: ${footerHeight}px. Pets bottom: ${petsBottomPosition}px.`);
    } else {
        console.warn("Elemento 'footer' não encontrado. Pets podem não aparecer na posição esperada.");
        // Valor padrão se não encontrar o rodapé, como antes
        petsBottomPosition = 20;
    }
    // --- Fim da nova lógica ---


    function animateAnimal(animal, callback) {
        const direction = Math.random() < 0.5 ? 1 : -1;
        let currentPosition;

        if (direction === 1) {
            currentPosition = -animal.offsetWidth;
        } else {
            currentPosition = screenWidth;
        }

        animal.style.display = 'block';
        animal.style.transform = `scaleX(${direction})`;
        // Define a posição vertical dos pets
        animal.style.bottom = `${petsBottomPosition}px`;

        function frame() {
            currentPosition += speed * direction;
            animal.style.left = `${currentPosition}px`;

            let hasExited;
            if (direction === 1) {
                hasExited = currentPosition > screenWidth;
            } else {
                hasExited = currentPosition < -animal.offsetWidth;
            }

            if (!hasExited) {
                requestAnimationFrame(frame);
            } else {
                animal.style.display = 'none';
                if (callback) callback();
            }
        }
        requestAnimationFrame(frame);
    }

    function startDogWalk() {
        animateAnimal(dog, function() {
            setTimeout(startDogWalk, Math.random() * 5000 + 3000);
        });
    }

    function startCatWalk() {
        animateAnimal(cat, function() {
            setTimeout(startCatWalk, Math.random() * 7000 + 5000);
        });
    }

    console.log("Iniciando animações de pets com direção aleatória e no rodapé...");
    setTimeout(startDogWalk, 2000);
    setTimeout(startCatWalk, 5000);

    dog.addEventListener('click', function() {
        alert('Au au! Bem-vindo à AgroFerragem!');
    });
    cat.addEventListener('click', function() {
        alert('Miau! AgroFerragem tem tudo para seu pet!');
    });
});