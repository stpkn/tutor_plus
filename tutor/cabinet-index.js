// Точка входа для личного кабинета (для React 16/17)
console.log('🔄 Загрузка Cabinet компонента...');

// Ждем загрузки DOM и React
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM загружен, рендерим Cabinet...');

    // Проверяем, что React и Cabinet доступны
    if (typeof React !== 'undefined' && typeof ReactDOM !== 'undefined' && typeof Cabinet !== 'undefined') {
        // Используем старый метод рендеринга для React 16/17
        ReactDOM.render(React.createElement(Cabinet), document.getElementById('root'));
        console.log('✅ Cabinet компонент отрендерен (React 16/17)');
    } else {
        console.error('❌ React или Cabinet не найдены');
        console.log('React:', typeof React);
        console.log('ReactDOM:', typeof ReactDOM);
        console.log('Cabinet:', typeof Cabinet);
    }
});