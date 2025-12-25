from obligations.models import Obligation

# Keep the first one, delete the rest
obligations = Obligation.objects.filter(title="Give back the book to her").order_by('created_at')
count = obligations.count()

if count > 1:
    # Get IDs of duplicates to delete
    first_id = obligations.first().id
    duplicate_ids = obligations.exclude(id=first_id).values_list('id', flat=True)
    
    # Delete duplicates
    deleted = Obligation.objects.filter(id__in=duplicate_ids).delete()
    print(f"Deleted {deleted[0]} duplicate obligations")
    print(f"Kept 1 obligation (ID: {first_id})")
else:
    print("No duplicates to clean up")
