document.addEventListener('DOMContentLoaded', function() {
    const dogWalker = document.getElementById('dog-walker');
    const catWalker = document.getElementById('cat-walker');

    // Configurações para os pets. x e y serão definidas dinamicamente.
    const pets = [
        {
            element: dogWalker,
            speed: 2,
            directionX: 1,
            directionY: 1,
            x: 0,
            y: 0,
            isVisible: false,
            currentTransform: 'scaleX(1)'
        },
        {
            element: catWalker,
            speed: 1.5,
            directionX: 1,
            directionY: 1,
            x: 0,
            y: 0,
            isVisible: false,
            currentTransform: 'scaleX(1)'
        }
    ];

    // Função para obter uma nova direção aleatória (-1 ou 1)
    function getRandomDirection() {
        return Math.random() < 0.5 ? 1 : -1;
    }

    function animatePets() {
        pets.forEach(pet => {
            if (!pet.isVisible || !pet.element) return; // Garante que o elemento existe e é visível

            // Atualiza posição X e Y
            pet.x += pet.speed * pet.directionX;
            pet.y += pet.speed * pet.directionY;

            // Define os limites da tela para o movimento
            const minX = 0;
            const maxX = window.innerWidth - pet.element.offsetWidth;
            const minY = 0;
            const footerHeight = document.querySelector('footer').offsetHeight || 0; // fallback para 0 se footer não for encontrado
            const maxY = window.innerHeight - footerHeight - pet.element.offsetHeight;

            let collided = false;

            // Colisão Horizontal
            if (pet.x > maxX) {
                pet.x = maxX;
                pet.directionX = -1;
                collided = true;
            } else if (pet.x < minX) {
                pet.x = minX;
                pet.directionX = 1;
                collided = true;
            }

            // Colisão Vertical
            if (pet.y > maxY) {
                pet.y = maxY;
                pet.directionY = -1;
                collided = true;
            } else if (pet.y < minY) {
                pet.y = minY;
                pet.directionY = 1;
                collided = true;
            }

            // Se houve colisão, sorteia uma nova direção para o eixo oposto
            if (collided) {
                if (Math.random() < 0.5) {
                    pet.directionY = getRandomDirection();
                } else {
                    pet.directionX = getRandomDirection();
                }
            }

            // Lógica para virar a imagem para a frente
            if (pet.directionX === -1 && pet.currentTransform !== 'scaleX(-1)') {
                pet.element.style.transform = 'scaleX(-1)';
                pet.currentTransform = 'scaleX(-1)';
            } else if (pet.directionX === 1 && pet.currentTransform !== 'scaleX(1)') {
                pet.element.style.transform = 'scaleX(1)';
                pet.currentTransform = 'scaleX(1)';
            }

            // Aplica as novas posições
            pet.element.style.left = pet.x + 'px';
            pet.element.style.top = pet.y + 'px';
        });

        requestAnimationFrame(animatePets);
    }

    // Função para controlar a visibilidade dos pets com base na rolagem e tamanho da tela
    let scrollTimeout;
    function handleScroll() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const scrollPosition = window.scrollY;
            const documentHeight = document.documentElement.scrollHeight;
            const windowHeight = window.innerHeight;
            const footerHeight = document.querySelector('footer').offsetHeight || 0;

            const showCondition = window.innerWidth > 768 && (scrollPosition + windowHeight) < (documentHeight - footerHeight);

            pets.forEach(pet => {
                if (showCondition) {
                    if (!pet.isVisible) {
                        pet.element.style.display = 'block';
                        pet.isVisible = true;
                        pet.element.style.transform = pet.currentTransform; // Aplica a transformação correta ao mostrar
                        
                        // Garante que a posição inicial seja setada corretamente ao aparecer
                        // Esta é uma tentativa de recalcular a posição se ele aparecer fora do lugar
                        const currentX = pet.element.offsetLeft;
                        const currentY = pet.element.offsetTop;
                        
                        const maxX = window.innerWidth - pet.element.offsetWidth;
                        const maxY = window.innerHeight - footerHeight - pet.element.offsetHeight;

                        // Se a posição atual for muito discrepante ou fora dos limites, tenta reposicionar aleatoriamente
                        if (currentX < 0 || currentX > maxX || currentY < 0 || currentY > maxY || (pet.x === 0 && pet.y === 0)) {
                             pet.x = Math.random() * maxX;
                             pet.y = Math.random() * maxY;
                             pet.element.style.left = pet.x + 'px';
                             pet.element.style.top = pet.y + 'px';
                        }
                    }
                } else {
                    if (pet.isVisible) {
                        pet.element.style.display = 'none';
                        pet.isVisible = false;
                    }
                }
            });
        }, 100);
    }

    // Event Listeners
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', () => {
        pets.forEach(pet => {
            if (pet.element && pet.isVisible) { // Ajusta apenas se o elemento existe e está visível
                const footerHeight = document.querySelector('footer').offsetHeight || 0;
                const maxX = window.innerWidth - pet.element.offsetWidth;
                const maxY = window.innerHeight - footerHeight - pet.element.offsetHeight;

                pet.x = Math.min(Math.max(pet.x, 0), maxX); // Garante que X esteja dentro dos limites
                pet.y = Math.min(Math.max(pet.y, 0), maxY); // Garante que Y esteja dentro dos limites
                
                pet.element.style.left = pet.x + 'px';
                pet.element.style.top = pet.y + 'px';
            }
        });
        handleScroll();
    });

    // --- MUDANÇAS CRUCIAIS AQUI ---
    // Inicializa a posição aleatória dos pets de forma mais robusta
    // Espera que as imagens estejam realmente carregadas para ter as dimensões corretas.
    window.addEventListener('load', () => {
        pets.forEach(pet => {
            if (pet.element && pet.element.complete) { // Verifica se a imagem já foi carregada
                const footerHeight = document.querySelector('footer').offsetHeight || 0;
                const maxX = window.innerWidth - pet.element.offsetWidth;
                const maxY = window.innerHeight - footerHeight - pet.element.offsetHeight;

                // Garante que maxX e maxY não sejam negativos (se o elemento for maior que a tela)
                const safeMaxX = Math.max(0, maxX);
                const safeMaxY = Math.max(0, maxY);

                pet.x = Math.random() * safeMaxX;
                pet.y = Math.random() * safeMaxY;

                pet.element.style.left = pet.x + 'px';
                pet.element.style.top = pet.y + 'px';

                // Define uma direção inicial aleatória para o movimento
                pet.directionX = getRandomDirection();
                pet.directionY = getRandomDirection();
                pet.currentTransform = (pet.directionX === -1) ? 'scaleX(-1)' : 'scaleX(1)';
                pet.element.style.transform = pet.currentTransform;
            } else if (pet.element) {
                // Se a imagem não estiver completa, adiciona um listener para carregar
                pet.element.addEventListener('load', () => {
                    const footerHeight = document.querySelector('footer').offsetHeight || 0;
                    const maxX = window.innerWidth - pet.element.offsetWidth;
                    const maxY = window.innerHeight - footerHeight - pet.element.offsetHeight;

                    const safeMaxX = Math.max(0, maxX);
                    const safeMaxY = Math.max(0, maxY);

                    pet.x = Math.random() * safeMaxX;
                    pet.y = Math.random() * safeMaxY;

                    pet.element.style.left = pet.x + 'px';
                    pet.element.style.top = pet.y + 'px';

                    pet.directionX = getRandomDirection();
                    pet.directionY = getRandomDirection();
                    pet.currentTransform = (pet.directionX === -1) ? 'scaleX(-1)' : 'scaleX(1)';
                    pet.element.style.transform = pet.currentTransform;

                    // Uma vez que todas as imagens estão carregadas, inicia a animação e o handleScroll
                    // (previne múltiplas chamadas se houver várias imagens)
                    const allImagesLoaded = pets.every(p => p.element.complete);
                    if (allImagesLoaded) {
                        handleScroll();
                        animatePets();
                    }
                });
            }
        });

        // Se todas as imagens já estiverem carregadas antes do 'load' disparar (cache, etc.)
        const allImagesLoadedImmediately = pets.every(p => p.element && p.element.complete);
        if (allImagesLoadedImmediately) {
             handleScroll();
             animatePets();
        }
    });

    // Chama handleScroll uma vez no DOMContentLoaded para configurar o display inicial
    handleScroll();
});