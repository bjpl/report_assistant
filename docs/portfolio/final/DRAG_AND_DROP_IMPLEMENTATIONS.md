# Drag and Drop Implementation Report

**Date:** October 18, 2025
**Projects with Drag and Drop:** 2 confirmed implementations
**Primary Library:** @dnd-kit/core
**Use Case:** Educational geography games

---

## Overview

This document details drag and drop functionality implementations in portfolio projects. Both implementations use the @dnd-kit library for accessible, touch-optimized drag and drop interactions.

---

## Projects with Drag and Drop Features

### 1. CALIFORNIA_PUZZLE_GAME - County Dragging System

**Library:** @dnd-kit/core with supporting packages

**Dependencies:**
```json
{
  "@dnd-kit/core": "^6.x",
  "@dnd-kit/utilities": "^3.x",
  "@dnd-kit/sortable": "^7.x",
  "@dnd-kit/modifiers": "^6.x"
}
```

**Implementation Architecture:**

**Draggable Elements:**
- 58 California county pieces
- County shapes rendered as SVG or images
- Visual feedback during drag operations
- Snap-to-grid on successful placement

**Drop Zones:**
- D3.js-generated map regions
- Precise boundary detection
- Visual highlighting on hover
- Collision detection for placement validation

**Core Features:**

1. **Touch Optimization:**
   - Native touch event support
   - Haptic feedback on successful drop
   - Gesture recognition for mobile devices
   - Minimum touch target size (48x48px)

2. **Accessibility:**
   - Keyboard navigation support
   - Screen reader announcements
   - ARIA labels for drag items
   - Focus management during drag operations
   - WCAG AA compliant

3. **Visual Feedback:**
   - Drag overlay during movement
   - Drop zone highlighting
   - Success/error animations
   - County outline preview on hover

4. **Game Mechanics:**
   - Validation on drop (correct/incorrect placement)
   - Score tracking per placement
   - Time tracking integration
   - Progressive difficulty levels

**Technical Implementation:**

```typescript
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent
} from '@dnd-kit/core';

function CaliforniaPuzzle() {
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // 8px movement before drag starts
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id === over.id) {
      // Successful placement
      validateCountyPlacement(active.id, over.id);
      playSuccessAnimation();
      updateScore();
    }
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <CountyTray counties={availableCounties} />
      <MapContainer regions={mapRegions} />
    </DndContext>
  );
}
```

**Collision Detection:**
```typescript
// Custom collision detection for map placement
const customCollisionDetection = (args) => {
  const pointerCollisions = pointerWithin(args);

  if (pointerCollisions.length > 0) {
    // Check if pointer is within county boundaries
    return pointerCollisions.filter(collision => {
      return isWithinCountyBounds(
        args.active.id,
        collision.id
      );
    });
  }

  return closestCenter(args);
};
```

**Performance Optimizations:**
- Virtual scrolling for county list
- Memoized collision calculations
- Debounced position updates
- RequestAnimationFrame for smooth dragging

---

### 2. COLOMBIA_PUZZLE_GAME - Department Dragging System

**Library:** @dnd-kit/core

**Implementation Scope:**
- 33 Colombian department pieces
- GeoJSON-based map regions
- Touch-optimized for mobile devices
- Multiple tray layouts (grid, list, regional)

**Core Features:**

1. **Department Selection:**
   - Drag departments from organized tray
   - Search/filter functionality
   - Regional grouping options
   - Visual categorization by region

2. **Placement Validation:**
   - GeoJSON boundary checking
   - Proximity-based suggestions
   - Error correction hints
   - Progressive hint system

3. **Touch Gestures:**
   - Long press to initiate drag
   - Pinch-to-zoom on map
   - Pan while dragging
   - Multi-touch support

4. **Visual Design:**
   - Department flag/emblem on pieces
   - Color-coded regions
   - Shadow effects during drag
   - Smooth transitions

**Technical Implementation:**

```typescript
interface DepartmentPiece {
  id: string;
  name: string;
  region: string;
  capital: string;
  bounds: GeoJSONPolygon;
}

function ColombiaPuzzle() {
  const [departments, setDepartments] = useState<DepartmentPiece[]>([]);
  const [placedDepartments, setPlacedDepartments] = useState<Set<string>>(new Set());

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (!over) return;

    const isCorrect = validateGeoJSONPlacement(
      active.data.current.bounds,
      over.data.current.bounds
    );

    if (isCorrect) {
      setPlacedDepartments(prev => new Set(prev).add(active.id));
      showSuccessFeedback();
    } else {
      showErrorFeedback();
      offerHint(active.id);
    }
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={customGeoJSONCollision}
      onDragEnd={handleDragEnd}
    >
      <DepartmentTray
        departments={departments.filter(d => !placedDepartments.has(d.id))}
      />
      <MapView
        placed={Array.from(placedDepartments)}
      />
    </DndContext>
  );
}
```

**GeoJSON Integration:**
```typescript
// Validate department placement using GeoJSON
function validateGeoJSONPlacement(
  draggedBounds: GeoJSONPolygon,
  targetBounds: GeoJSONPolygon
): boolean {
  // Use turf.js for geometric calculations
  const draggedPolygon = polygon(draggedBounds.coordinates);
  const targetPolygon = polygon(targetBounds.coordinates);

  // Check if centroids are close
  const draggedCenter = centroid(draggedPolygon);
  const targetCenter = centroid(targetPolygon);
  const distance = turf.distance(draggedCenter, targetCenter);

  return distance < PLACEMENT_THRESHOLD;
}
```

**Hint System Integration:**
```typescript
function offerHint(departmentId: string) {
  const department = departments.find(d => d.id === departmentId);

  switch (hintLevel) {
    case 'region':
      highlightRegion(department.region);
      break;
    case 'neighbor':
      highlightNeighbors(departmentId);
      break;
    case 'flash':
      flashCorrectLocation(departmentId, 2000);
      break;
  }
}
```

---

## Common Implementation Patterns

### Accessibility Features

**Keyboard Navigation:**
```typescript
const keyboardSensor = useSensor(KeyboardSensor, {
  coordinateGetter: (event, { active, currentCoordinates }) => {
    // Arrow keys move 10px per press
    switch (event.code) {
      case 'ArrowUp':
        return { x: currentCoordinates.x, y: currentCoordinates.y - 10 };
      case 'ArrowDown':
        return { x: currentCoordinates.x, y: currentCoordinates.y + 10 };
      case 'ArrowLeft':
        return { x: currentCoordinates.x - 10, y: currentCoordinates.y };
      case 'ArrowRight':
        return { x: currentCoordinates.x + 10, y: currentCoordinates.y };
    }
  }
});
```

**Screen Reader Support:**
```typescript
<Draggable
  id={county.id}
  aria-label={`${county.name} county, drag to place on map`}
  aria-describedby="drag-instructions"
  role="button"
  tabIndex={0}
>
  {county.name}
</Draggable>
```

### Performance Optimizations

**Virtualization:**
```typescript
// Virtual scrolling for large lists
import { useVirtualizer } from '@tanstack/react-virtual';

const rowVirtualizer = useVirtualizer({
  count: counties.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 60, // 60px per item
  overscan: 5 // Render 5 extra items
});
```

**Memoization:**
```typescript
// Prevent unnecessary re-renders
const DraggableCounty = memo(({ county }: { county: County }) => {
  return (
    <Draggable id={county.id}>
      <CountyCard {...county} />
    </Draggable>
  );
}, (prev, next) => prev.county.id === next.county.id);
```

### Touch Optimization

**Activation Constraints:**
```typescript
useSensor(PointerSensor, {
  activationConstraint: {
    distance: 8,  // Prevent accidental drags
    delay: 100,   // 100ms delay for long press
    tolerance: 5  // Allow 5px movement during delay
  }
});
```

**Haptic Feedback:**
```typescript
function playHapticFeedback(type: 'light' | 'medium' | 'heavy') {
  if ('vibrate' in navigator) {
    switch (type) {
      case 'light':
        navigator.vibrate(10);
        break;
      case 'medium':
        navigator.vibrate(20);
        break;
      case 'heavy':
        navigator.vibrate([20, 10, 20]);
        break;
    }
  }
}
```

---

## Testing Strategies

### Unit Tests
```typescript
describe('Drag and Drop', () => {
  it('validates correct county placement', () => {
    const result = validateCountyPlacement('alameda', 'alameda-region');
    expect(result).toBe(true);
  });

  it('rejects incorrect placement', () => {
    const result = validateCountyPlacement('alameda', 'san-diego-region');
    expect(result).toBe(false);
  });

  it('handles drag cancel', () => {
    const { getByRole } = render(<PuzzleGame />);
    const county = getByRole('button', { name: /alameda/i });

    fireEvent.keyDown(county, { key: 'Escape' });
    expect(county).toHaveAttribute('aria-grabbed', 'false');
  });
});
```

### E2E Tests
```typescript
// Playwright test
test('completes puzzle with drag and drop', async ({ page }) => {
  await page.goto('/california-puzzle');

  // Drag first county
  const county = page.locator('[data-county="alameda"]');
  const target = page.locator('[data-region="alameda-region"]');

  await county.dragTo(target);

  // Verify placement
  await expect(page.locator('.success-message')).toBeVisible();
  await expect(page.locator('[data-placed="alameda"]')).toBeVisible();
});
```

---

## Mobile Considerations

### Responsive Layouts
- Tray collapses to bottom drawer on mobile
- Map scales to fit viewport
- Touch targets minimum 48x48px
- Swipe gestures for tray navigation

### Performance on Mobile
- Reduced animation complexity
- Throttled position updates (60fps)
- Simplified collision detection
- Progressive enhancement for older devices

---

## Known Limitations and Solutions

### Browser Compatibility
- iOS Safari: Custom touch event handling
- Android Chrome: Scroll prevention during drag
- Firefox: Performance optimization for large maps

### Edge Cases
- Multiple simultaneous touches: Queue system
- Drag outside viewport: Auto-scroll implementation
- Rapid drag/drop: Debouncing validation
- Network lag: Optimistic UI updates

---

## Future Enhancements

### California Puzzle
- Multiplayer mode with real-time sync
- County rotation for harder difficulty
- Time trial mode with leaderboards
- Custom puzzle creation

### Colombia Puzzle
- 3D map view option
- AR placement mode
- Voice guidance for accessibility
- Regional challenges

---

## Summary

Drag and drop implementations across both puzzle games demonstrate:

1. **Accessibility:** Keyboard navigation, screen reader support, WCAG AA compliance
2. **Touch Optimization:** Haptic feedback, gesture recognition, mobile-first design
3. **Performance:** Virtual scrolling, memoization, throttled updates
4. **Game Integration:** Validation systems, hint mechanisms, progress tracking
5. **Cross-Platform:** Desktop and mobile support with responsive layouts

Both implementations use @dnd-kit for:
- Accessible drag and drop interactions
- Touch and pointer event handling
- Collision detection algorithms
- Keyboard sensor integration
- Flexible drag overlay system

---

*End of Drag and Drop Implementation Report*