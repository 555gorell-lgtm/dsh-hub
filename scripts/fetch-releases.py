---
import Base from '../layouts/Base.astro';
import PluginCard from '../components/PluginCard.astro';
import plugins from '../data/plugins.json';
const categories = [...new Set(plugins.map(p => p.category))];
---
<Base title="Каталог — PluginHub">
  <h1>Каталог плагинов</h1>

  <div class="filters">
    <button class="filter active" data-cat="">Все</button>
    {categories.map(c => <button class="filter" data-cat={c}>{c}</button>)}
  </div>

  <div class="grid" id="catalog">
    {plugins.map(p => <PluginCard plugin={p} />)}
  </div>
</Base>

<script>
  document.querySelectorAll('.filter').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.cat;
      document.querySelectorAll('#catalog .card').forEach(card => {
        card.style.display = (!cat || card.dataset.category === cat) ? '' : 'none';
      });
    });
  });
</script>
