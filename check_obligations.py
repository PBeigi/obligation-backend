from obligations.models import Obligation

print(f'Total obligations: {Obligation.objects.count()}')
print()
for i, o in enumerate(Obligation.objects.all(), 1):
    print(f'{i}. "{o.title}" - {o.status}')
    print(f'   Owed by: {o.owed_by.email}')
    print(f'   Owed to: {o.owed_to.email}')
    print(f'   Created: {o.created_at}')
    print()
