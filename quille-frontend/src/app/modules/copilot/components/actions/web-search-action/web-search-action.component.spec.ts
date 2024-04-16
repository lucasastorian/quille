import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebSearchActionComponent } from './web-search-action.component';

describe('WebSearchActionComponent', () => {
  let component: WebSearchActionComponent;
  let fixture: ComponentFixture<WebSearchActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WebSearchActionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(WebSearchActionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
