
#include <cassert>
#include <cstdio>
#include <vector>
#include <queue>


//
// Вершина
//
class node {
public:

	// Ребро
	class linkage {
	public:
		node* dst;
		int weight;

		// Конструктор
		linkage(node* dst, int weight) : dst(dst), weight(weight) {
		}
	};

	std::vector<linkage> connected;
	bool seen = false;
	int cost = 9999;
	int name = 0;

	node* back = nullptr;

	// Конструктор
	node(int name) : name(name) {
	}
};

//
// Граф
//
class graph {
public:
	std::vector<node*> nodes;

	node* node_by_name(int name) {
		for (node* it : nodes) {
			if ( it->name == name )
				return it;
		}
		return nullptr;
	}

	node* add_node(int name) {
		node* result = new node(name);
		nodes.push_back(result);
		return result;
	}
};

class node_prio_queue_entry {
public:
	node* node_ptr;

	// Конструктор
	node_prio_queue_entry(node* node_ptr) : node_ptr(node_ptr) {
	}

	// Для упорядочивания
	bool operator<(const node_prio_queue_entry& other) const {
		return node_ptr->cost > other.node_ptr->cost;
	}
};

//
// Дейкстра
//
void walk(node* init, node* target) {
	std::priority_queue<node_prio_queue_entry> queue;

	init->cost = 0;

	queue.push( node_prio_queue_entry(init) );

	// Пробежка
	while (!queue.empty()) {
		node_prio_queue_entry const& e = queue.top();
		node* loc = e.node_ptr;
		queue.pop();

		loc->seen = true;

		printf("In node(%d) cost %d\n", loc->name, loc->cost);

		for (node::linkage link : loc->connected) {
			node* dst = link.dst;

			if (dst->seen)
				continue;

			int cost_from_here = loc->cost + link.weight;

			if (cost_from_here < dst->cost) {
				dst->cost = cost_from_here;
				dst->back = loc;
			}

			printf("Establish that node(%d) cost %d\n", dst->name, dst->cost);

			queue.push( node_prio_queue_entry(link.dst) );
		}
	}

	printf("Path from %d to %d costs %d\n", init->name, target->name, target->cost);

	// Пробежка от цели к началу
	std::vector<node*> history;
	node* loc = target;

	while (1) {
		history.push_back(loc);
		loc = loc->back;
		if (!loc) break;
	}

	for (auto it = history.rbegin(); it != history.rend(); it++) {
		printf("%d ", (*it)->name);
	}

	printf("End\n");
}

int main() {
	FILE* fd = fopen("dijkstra/edgelist.txt", "r");
	graph g;

	while (!feof(fd)) {
		int a, b, w;

		int rc = fscanf(fd, "%d,%d,%d\n", &a, &b, &w);

		assert(rc == 3);

		node* a_ = g.node_by_name(a);
		node* b_ = g.node_by_name(b);

		if (!a_)
			a_ = g.add_node(a);

		if (!b_)
			b_ = g.add_node(b);

		a_->connected.push_back( node::linkage(b_, w) );
	}

	walk( g.node_by_name(1), g.node_by_name(9) );
}
