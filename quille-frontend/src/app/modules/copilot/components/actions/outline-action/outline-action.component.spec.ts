import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OutlineActionComponent } from './outline-action.component';

describe('OutlineActionComponent', () => {
  let component: OutlineActionComponent;
  let fixture: ComponentFixture<OutlineActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OutlineActionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OutlineActionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
